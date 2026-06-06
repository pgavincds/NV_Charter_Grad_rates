#!/usr/bin/env python3

from __future__ import annotations

import csv
import hashlib
import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


HOME = Path("/Users/patrickgavin")
WORKSPACE = Path("/Users/patrickgavin/Documents/New project")
OUTPUT_DIR = WORKSPACE / "historical_graduation_rate_artifact_universe"
MIRROR_DIR = OUTPUT_DIR / "mirror"
MANIFEST_PATH = OUTPUT_DIR / "manifest.csv"
README_PATH = OUTPUT_DIR / "README.md"
ERRORS_PATH = OUTPUT_DIR / "errors.csv"

SEARCH_ROOTS = [
    HOME / "Desktop",
    HOME / "Documents",
    HOME / "Downloads",
    HOME / "Google Drive",
    HOME / "NAEP-charter-analysis",
    HOME / "Library" / "Mobile Documents",
    HOME / "Library" / "CloudStorage",
]

READ_FALLBACK_ROOTS = {
    HOME / "Library" / "CloudStorage" / "OneDrive-CharterDevelopmentStrategies": (
        HOME
        / "Library"
        / "Group Containers"
        / "UBF8T346G9.OneDriveStandaloneSuite"
        / "OneDrive - Charter Development Strategies.noindex"
        / "OneDrive - Charter Development Strategies"
    ),
}

SPREADSHEET_EXTS = {".csv", ".xls", ".xlsx"}
CUTOFF_TS = datetime(2020, 1, 1, tzinfo=timezone.utc).timestamp()

GRAD_KEYWORDS = [
    "graduat",
    "grad rate",
    "grad_rate",
    "acgr",
    "cohort",
    "dropout",
    "completion",
]

EDU_KEYWORDS = [
    "charter",
    "school",
    "student",
    "district",
    "nces",
    "ipeds",
    "edfacts",
    "ccd",
]

NEVADA_CROSSCHECK_KEYWORDS = [
    "numberofstudent",
    "validation_day_student_counts",
    "enrollment_numbers",
    "membbyschoolbygrade",
    "district headcount by grade",
]

PATH_KEYWORDS = GRAD_KEYWORDS + EDU_KEYWORDS + NEVADA_CROSSCHECK_KEYWORDS
PATH_REGEX = re.compile("|".join(re.escape(k) for k in PATH_KEYWORDS), re.IGNORECASE)
CSV_CONTENT_REGEX = re.compile(
    r"graduat|grad[ _-]?rate|acgr|cohort|dropout|completion|on[ _-]?time",
    re.IGNORECASE,
)

EXCLUDE_PREFIXES = [
    WORKSPACE,
    OUTPUT_DIR,
]


@dataclass
class Candidate:
    source_path: Path
    read_path: Path
    mirror_rel_path: Path
    size_bytes: int
    modified_at_utc: str
    sha256: str
    reason_pre2020: bool
    reason_path_keyword: bool
    reason_csv_content_keyword: bool
    path_keyword_hits: str


def is_excluded(path: Path) -> bool:
    path = path.resolve()
    for prefix in EXCLUDE_PREFIXES:
        prefix = prefix.resolve()
        if path == prefix or prefix in path.parents:
            return True
    return False


def iter_spreadsheets():
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dir_path = Path(dirpath)
            if is_excluded(dir_path):
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if not is_excluded(dir_path / d)]
            for filename in filenames:
                path = dir_path / filename
                if path.suffix.lower() not in SPREADSHEET_EXTS:
                    continue
                if is_excluded(path):
                    continue
                yield path


def find_path_keyword_hits(path: Path) -> list[str]:
    lower_path = str(path).lower()
    hits = [keyword for keyword in PATH_KEYWORDS if keyword in lower_path]
    return sorted(set(hits))


def read_path_options(path: Path) -> list[Path]:
    options = [path]
    for primary_root, fallback_root in READ_FALLBACK_ROOTS.items():
        try:
            rel = path.relative_to(primary_root)
        except ValueError:
            continue
        options.append(fallback_root / rel)
    return options


def first_readable_path(path: Path) -> Path:
    errors: list[OSError] = []
    for candidate in read_path_options(path):
        try:
            with candidate.open("rb") as handle:
                handle.read(1)
                return candidate
        except OSError as exc:
            errors.append(exc)
    raise errors[-1]


def csv_has_grad_content(path: Path) -> bool:
    if path.suffix.lower() != ".csv":
        return False
    for candidate in read_path_options(path):
        try:
            with candidate.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), ""):
                    if CSV_CONTENT_REGEX.search(chunk):
                        return True
            return False
        except OSError:
            continue
    return False


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def home_relative_path(path: Path) -> Path:
    return path.relative_to(HOME)


def collect_candidates() -> tuple[list[Candidate], list[dict[str, str]]]:
    candidates: list[Candidate] = []
    errors: list[dict[str, str]] = []
    seen: set[Path] = set()

    for path in iter_spreadsheets():
        try:
            resolved = path.resolve()
        except OSError:
            resolved = path
        if resolved in seen:
            continue
        seen.add(resolved)

        try:
            stat = path.stat()
        except OSError as exc:
            errors.append({"source_path": str(path), "error": f"stat failed: {exc}"})
            continue

        reason_pre2020 = stat.st_mtime < CUTOFF_TS
        path_hits = find_path_keyword_hits(path)
        reason_path_keyword = bool(path_hits)
        reason_csv_content_keyword = csv_has_grad_content(path)

        if not any([reason_pre2020, reason_path_keyword, reason_csv_content_keyword]):
            continue

        try:
            read_path = first_readable_path(path)
            sha256 = sha256_for_file(read_path)
        except OSError as exc:
            errors.append({"source_path": str(path), "error": f"hash failed: {exc}"})
            continue

        modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
        candidates.append(
            Candidate(
                source_path=path,
                read_path=read_path,
                mirror_rel_path=home_relative_path(path),
                size_bytes=stat.st_size,
                modified_at_utc=modified_at,
                sha256=sha256,
                reason_pre2020=reason_pre2020,
                reason_path_keyword=reason_path_keyword,
                reason_csv_content_keyword=reason_csv_content_keyword,
                path_keyword_hits=";".join(path_hits),
            )
        )

    candidates.sort(key=lambda item: str(item.source_path).lower())
    return candidates, errors


def write_manifest(candidates: list[Candidate]) -> None:
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_path",
                "read_path",
                "mirror_rel_path",
                "size_bytes",
                "modified_at_utc",
                "sha256",
                "reason_pre2020",
                "reason_path_keyword",
                "reason_csv_content_keyword",
                "path_keyword_hits",
            ],
        )
        writer.writeheader()
        for item in candidates:
            writer.writerow(
                {
                    "source_path": str(item.source_path),
                    "read_path": str(item.read_path),
                    "mirror_rel_path": str(item.mirror_rel_path),
                    "size_bytes": item.size_bytes,
                    "modified_at_utc": item.modified_at_utc,
                    "sha256": item.sha256,
                    "reason_pre2020": int(item.reason_pre2020),
                    "reason_path_keyword": int(item.reason_path_keyword),
                    "reason_csv_content_keyword": int(item.reason_csv_content_keyword),
                    "path_keyword_hits": item.path_keyword_hits,
                }
            )


def write_errors(errors: list[dict[str, str]]) -> None:
    with ERRORS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_path", "error"])
        writer.writeheader()
        writer.writerows(errors)


def copy_candidates(candidates: list[Candidate]) -> None:
    for item in candidates:
        destination = MIRROR_DIR / item.mirror_rel_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item.read_path, destination)


def build_readme(candidates: list[Candidate], errors: list[dict[str, str]]) -> None:
    total_size = sum(item.size_bytes for item in candidates)
    reason_counts = Counter()
    root_counts = Counter()

    for item in candidates:
        if item.reason_pre2020:
            reason_counts["pre2020"] += 1
        if item.reason_path_keyword:
            reason_counts["path_keyword"] += 1
        if item.reason_csv_content_keyword:
            reason_counts["csv_content_keyword"] += 1
        root_counts[item.mirror_rel_path.parts[0]] += 1

    lines = [
        "# Historical Graduation Rate Artifact Universe",
        "",
        "This folder contains mirrored copies of spreadsheet-like files that may be part of prior graduation-rate work.",
        "",
        "Inclusion rules:",
        "- Spreadsheet extension: `.csv`, `.xls`, or `.xlsx`.",
        "- Modified before `2020-01-01` UTC, or",
        "- Path contains education/graduation-related keywords, or",
        "- CSV content contains graduation-related keywords.",
        "",
        "Search roots:",
    ]
    lines.extend(f"- `{root}`" for root in SEARCH_ROOTS if root.exists())
    lines.extend(
        [
            "",
            "Explicit exclusions:",
            f"- `{WORKSPACE}`",
            "",
            "Summary:",
            f"- Candidate files mirrored: `{len(candidates)}`",
            f"- Total mirrored size: `{round(total_size / 1024 / 1024, 2)}` MB",
            f"- Files matched by pre-2020 timestamp: `{reason_counts['pre2020']}`",
            f"- Files matched by path keyword: `{reason_counts['path_keyword']}`",
            f"- Files matched by CSV content keyword: `{reason_counts['csv_content_keyword']}`",
            f"- Files with copy/hash/stat errors: `{len(errors)}`",
            "",
            "Top root buckets:",
        ]
    )
    for root_name, count in root_counts.most_common():
        lines.append(f"- `{root_name}`: `{count}` files")

    lines.extend(
        [
            "",
            "Files:",
            "- `mirror/` preserves paths relative to `/Users/patrickgavin`.",
            "- `manifest.csv` lists every source file, mirrored relative path, reasons, size, timestamp, and SHA-256 hash.",
            "- `read_path` in the manifest shows when a local cache path was used to recover a cloud placeholder.",
            "- `errors.csv` records any files that could not be processed.",
        ]
    )

    README_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if MIRROR_DIR.exists():
        shutil.rmtree(MIRROR_DIR)
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)

    candidates, errors = collect_candidates()
    write_manifest(candidates)
    write_errors(errors)
    copy_candidates(candidates)
    build_readme(candidates, errors)

    print(f"candidate_files={len(candidates)}")
    print(f"manifest={MANIFEST_PATH}")
    print(f"mirror={MIRROR_DIR}")
    print(f"errors={len(errors)}")


if __name__ == "__main__":
    main()
