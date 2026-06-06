#!/usr/bin/env python3

from __future__ import annotations

import csv
import re
import shutil
import zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


HOME = Path("/Users/patrickgavin")
WORKSPACE = Path("/Users/patrickgavin/Documents/New project")
UNIVERSE_MANIFEST = WORKSPACE / "historical_graduation_rate_artifact_universe" / "manifest.csv"
TRACKER_CSV = WORKSPACE / "nevada_grade12_enrollment_crosscheck_sources.csv"

OUTPUT_DIR = WORKSPACE / "historical_graduation_rate_artifact_focus"
MIRROR_DIR = OUTPUT_DIR / "mirror"
FOCUS_MANIFEST = OUTPUT_DIR / "focus_manifest.csv"
TRACKER_CROSSWALK = OUTPUT_DIR / "source_tracker_crosswalk.csv"
README = OUTPUT_DIR / "README.md"

CSV_PREVIEW_LINES = 3


def normalize_name(name: str) -> str:
    stem = re.sub(r"\.[^.]+$", "", name)
    parts = re.split(r"[_\-\s]+", stem)
    while parts and re.fullmatch(r"[0-9a-f]{6,}", parts[-1], re.IGNORECASE):
        parts.pop()
    return re.sub(r"[^a-z0-9]+", "", "".join(parts).lower())


def path_rank(path: Path) -> tuple[int, int, str]:
    text = str(path)
    prefixes = [
        "/Users/patrickgavin/Documents/Takeout_Unzipped",
        "/Users/patrickgavin/Documents/PJG Drive Files",
        "/Users/patrickgavin/Documents",
        "/Users/patrickgavin/Downloads",
        "/Users/patrickgavin/Library/Mobile Documents/com~apple~CloudDocs",
        "/Users/patrickgavin/Library/CloudStorage",
    ]
    for idx, prefix in enumerate(prefixes):
        if text.startswith(prefix):
            return (idx, len(path.name), text.lower())
    return (len(prefixes), len(path.name), text.lower())


def choose_primary(paths: list[Path], preferred_name: str | None = None) -> Path:
    ranked = sorted(paths, key=path_rank)
    if preferred_name:
        preferred = [path for path in ranked if path.name == preferred_name]
        if preferred:
            return preferred[0]
    return ranked[0]


def csv_preview(path: Path) -> str:
    lines: list[str] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
            for _ in range(CSV_PREVIEW_LINES):
                line = handle.readline()
                if not line:
                    break
                lines.append(line.strip())
    except OSError as exc:
        return f"preview failed: {exc}"
    return " || ".join(lines)


def xlsx_sheet_names(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            workbook = archive.read("xl/workbook.xml").decode("utf-8", "ignore")
    except Exception as exc:
        return f"sheet read failed: {exc}"
    names = re.findall(r'<sheet[^>]*name="([^"]+)"', workbook)
    return ", ".join(names[:8])


def xlsx_snippet(path: Path, pattern: str) -> str:
    regex = re.compile(rf".{{0,80}}{pattern}.{{0,180}}", re.IGNORECASE | re.DOTALL)
    try:
        with zipfile.ZipFile(path) as archive:
            texts = []
            for name in archive.namelist():
                if name.endswith(".xml") and (
                    "sharedStrings" in name or "sheet" in name or "workbook" in name
                ):
                    texts.append(archive.read(name).decode("utf-8", "ignore"))
    except Exception as exc:
        return f"snippet failed: {exc}"
    match = regex.search(" ".join(texts))
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(0)).strip()


def home_relative(path: Path) -> Path:
    return path.relative_to(HOME)


def load_manifest_rows() -> list[dict[str, str]]:
    with UNIVERSE_MANIFEST.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_tracker_rows() -> list[dict[str, str]]:
    with TRACKER_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def make_focus_record(
    row: dict[str, str],
    focus_label: str,
    focus_group: str,
    confidence: str,
    workspace_linkage: str,
    evidence: str,
    source_tracker_match: str = "",
    primary_copy: bool = False,
) -> dict[str, str]:
    source_path = Path(row["source_path"])
    return {
        "focus_label": focus_label,
        "focus_group": focus_group,
        "confidence": confidence,
        "workspace_linkage": workspace_linkage,
        "source_tracker_match": source_tracker_match,
        "primary_copy": "1" if primary_copy else "0",
        "source_path": str(source_path),
        "read_path": row["read_path"],
        "mirror_rel_path": str(home_relative(source_path)),
        "sha256": row["sha256"],
        "evidence": evidence,
    }


def main() -> None:
    manifest_rows = load_manifest_rows()
    tracker_rows = load_tracker_rows()

    rows_by_path = {row["source_path"]: row for row in manifest_rows}
    all_paths = [Path(row["source_path"]) for row in manifest_rows]
    norm_index = [(normalize_name(path.name), path) for path in all_paths]

    selected: dict[tuple[str, str], dict[str, str]] = {}
    crosswalk_rows: list[dict[str, str]] = []

    def add_records(
        paths: list[Path],
        focus_label: str,
        focus_group: str,
        confidence: str,
        workspace_linkage: str,
        evidence: str,
        source_tracker_match: str = "",
        preferred_name: str | None = None,
    ) -> None:
        if not paths:
            return
        unique_paths = sorted(set(paths), key=path_rank)
        primary = choose_primary(unique_paths, preferred_name=preferred_name)
        for path in unique_paths:
            row = rows_by_path[str(path)]
            record = make_focus_record(
                row=row,
                focus_label=focus_label,
                focus_group=focus_group,
                confidence=confidence,
                workspace_linkage=workspace_linkage,
                evidence=evidence,
                source_tracker_match=source_tracker_match,
                primary_copy=(path == primary),
            )
            selected[(focus_label, str(path))] = record

    for tracker in tracker_rows:
        source_url = tracker["enrollment_source_url"]
        source_base = Path(urlparse(source_url).path).name
        tracker_core = normalize_name(source_base)
        matches = [
            path
            for norm_name, path in norm_index
            if tracker_core and (tracker_core in norm_name or norm_name in tracker_core)
        ]
        primary = choose_primary(matches, preferred_name=source_base) if matches else None
        status = "not_found"
        if matches:
            status = "found_local_match"
            add_records(
                paths=matches,
                focus_label=tracker["source_label"],
                focus_group="enrollment_crosscheck",
                confidence="high",
                workspace_linkage="nevada_grade12_enrollment_crosscheck_sources.csv",
                evidence=f"Sheets: {xlsx_sheet_names(primary)}",
                source_tracker_match=tracker["school_year"],
                preferred_name=source_base,
            )
        crosswalk_rows.append(
            {
                "school_year": tracker["school_year"],
                "source_label": tracker["source_label"],
                "source_url": source_url,
                "match_status": status,
                "primary_local_path": str(primary) if primary else "",
                "matched_local_paths": " || ".join(str(path) for path in sorted(matches, key=path_rank)),
                "notes": tracker["notes"],
            }
        )

    supplemental_files = [
        (
            "2021 Membership by School by Grade",
            "enrollment_support",
            "medium",
            "Supplemental Nevada enrollment support",
            "2021MembBySchoolByGrade.xlsx",
            "Sheets: State-District, Schl Total Enrollment, School",
        ),
        (
            "District Headcount by Grade",
            "enrollment_support",
            "medium",
            "Supplemental Nevada enrollment support",
            "District Headcount by Grade.xlsx",
            "Sheets: district by grade",
        ),
    ]
    for label, group, confidence, linkage, basename, evidence in supplemental_files:
        matches = [path for path in all_paths if path.name == basename]
        add_records(
            paths=matches,
            focus_label=label,
            focus_group=group,
            confidence=confidence,
            workspace_linkage=linkage,
            evidence=evidence,
            preferred_name=basename,
        )

    summary_definitions = [
        (
            "State + SPCSA Cohort 4Yr Graduation Summary",
            "direct_grad_summary",
            "high",
            "Reusable direct graduation summary CSV",
            {"Grads.csv", "grdc.csv"},
            'Preview: "Group Summary Report" || "Cohort 4Yr Graduation Rates (Reported for Prior School Year)"',
            "Grads.csv",
        ),
        (
            "Clark Cohort 4Yr Graduation Summary",
            "direct_grad_summary",
            "high",
            "Reusable direct graduation summary CSV",
            {"Clark.csv"},
            'Preview: "Group Summary Report" || "Cohort 4Yr Graduation Rates (Reported for Prior School Year)"',
            "Clark.csv",
        ),
        (
            "Washoe Cohort 4Yr Graduation Summary",
            "direct_grad_summary",
            "high",
            "Reusable direct graduation summary CSV",
            {"wshgr.csv"},
            'Preview: "Group Summary Report" || "Cohort 4Yr Graduation Rates (Reported for Prior School Year)"',
            "wshgr.csv",
        ),
    ]
    for label, group, confidence, linkage, basenames, evidence, preferred in summary_definitions:
        matches = [path for path in all_paths if path.name in basenames]
        add_records(
            paths=matches,
            focus_label=label,
            focus_group=group,
            confidence=confidence,
            workspace_linkage=linkage,
            evidence=evidence,
            preferred_name=preferred,
        )

    survey_paths = [
        path
        for path in all_paths
        if path.name == "Sheet_1.csv" and "Data_All_160819" in str(path)
    ]
    add_records(
        paths=survey_paths,
        focus_label="2016 Nevada Charter Dual Enrollment Survey Export",
        focus_group="historical_direct_evidence",
        confidence="high",
        workspace_linkage="Historical survey export with ACGR questions",
        evidence=(
            "Header includes: "
            '"What was your charter school\'s adjusted cohort graduation rate as reported by the Nevada Department of Education in each of the past three years"'
        ),
        preferred_name="Sheet_1.csv",
    )

    old_schoolratings = [
        path
        for path in all_paths
        if str(path).endswith("Consolidated_Mac_Downloads/SchoolRatings.csv")
    ]
    add_records(
        paths=old_schoolratings,
        focus_label="Historical SchoolRatings Export",
        focus_group="historical_direct_evidence",
        confidence="high",
        workspace_linkage="Historical Nevada school ratings export",
        evidence="Header contains 4-Year Graduation Rate and 5-Year Graduation Rate columns; first data year is 2018.",
        preferred_name="SchoolRatings.csv",
    )

    current_schoolratings = [
        path
        for path in all_paths
        if path.name == "SchoolRatings.csv"
        and (
            str(path).startswith("/Users/patrickgavin/Downloads/")
            or str(path).startswith("/Users/patrickgavin/Library/Mobile Documents/com~apple~CloudDocs/")
        )
    ]
    add_records(
        paths=current_schoolratings,
        focus_label="Later SchoolRatings Export",
        focus_group="later_support_files",
        confidence="medium",
        workspace_linkage="Later Nevada school ratings export",
        evidence="Header contains 4-Year Graduation Rate and 5-Year Graduation Rate columns; first visible data year is 2024.",
        preferred_name="SchoolRatings.csv",
    )

    spcsa_2015 = [
        path
        for path in all_paths
        if path.name == "SPCSA 2015 Legislative Report.xlsx"
    ]
    add_records(
        paths=spcsa_2015,
        focus_label="SPCSA 2015 Legislative Report",
        focus_group="policy_context",
        confidence="medium",
        workspace_linkage="Historical Nevada charter policy context",
        evidence=xlsx_snippet(spcsa_2015[0], "graduation rate") if spcsa_2015 else "",
        preferred_name="SPCSA 2015 Legislative Report.xlsx",
    )

    roles_paths = [
        path
        for path in all_paths
        if path.name == "Charter School Organizational Roles.xlsx"
    ]
    add_records(
        paths=roles_paths,
        focus_label="Charter School Organizational Roles",
        focus_group="operational_context",
        confidence="medium",
        workspace_linkage="Operational graduation-rate workflow context",
        evidence=xlsx_snippet(roles_paths[0], "Graduation Rate Validation Coordinator") if roles_paths else "",
        preferred_name="Charter School Organizational Roles.xlsx",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if MIRROR_DIR.exists():
        shutil.rmtree(MIRROR_DIR)
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)

    for record in selected.values():
        source_path = Path(record["read_path"])
        destination = MIRROR_DIR / record["mirror_rel_path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)

    focus_rows = sorted(
        selected.values(),
        key=lambda row: (
            row["focus_group"],
            row["focus_label"],
            row["primary_copy"] != "1",
            row["source_path"].lower(),
        ),
    )
    with FOCUS_MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "focus_label",
                "focus_group",
                "confidence",
                "workspace_linkage",
                "source_tracker_match",
                "primary_copy",
                "source_path",
                "read_path",
                "mirror_rel_path",
                "sha256",
                "evidence",
            ],
        )
        writer.writeheader()
        writer.writerows(focus_rows)

    with TRACKER_CROSSWALK.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "school_year",
                "source_label",
                "source_url",
                "match_status",
                "primary_local_path",
                "matched_local_paths",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(crosswalk_rows)

    group_counts = Counter(row["focus_group"] for row in focus_rows)
    found_years = [row["school_year"] for row in crosswalk_rows if row["match_status"] != "not_found"]
    missing_years = [row["school_year"] for row in crosswalk_rows if row["match_status"] == "not_found"]
    primary_count = sum(1 for row in focus_rows if row["primary_copy"] == "1")

    readme_lines = [
        "# Historical Graduation Rate Artifact Focus",
        "",
        "This folder is a tighter cut of the broader artifact universe.",
        "",
        "What is here:",
        f"- Focused files mirrored: `{len(focus_rows)}`",
        f"- Primary artifacts / file families: `{primary_count}`",
        "- The mirror preserves original paths relative to `/Users/patrickgavin`.",
        "",
        "Key findings:",
        "- The strongest historical hit is the 2016 Nevada charter dual-enrollment survey export, which directly asks schools for their adjusted cohort graduation rates for 2013, 2014, and 2015.",
        "- A historical `SchoolRatings.csv` export from 2018 carries both `4-Year Graduation Rate` and `5-Year Graduation Rate` columns.",
        "- Direct group-summary graduation CSVs are present for statewide/SPCSA, Clark, and Washoe.",
        "- The Nevada grade-12 crosscheck spreadsheet chain is locally present from 2017-2018 through 2024-2025, with 2015-2016 and 2016-2017 not found.",
        "- The 2022-2023 enrollment file existed locally but required explicit filename matching to pull into the universe.",
        "",
        "Focus groups:",
    ]
    for group, count in sorted(group_counts.items()):
        readme_lines.append(f"- `{group}`: `{count}` files")
    readme_lines.extend(
        [
            "",
            "Crosscheck coverage:",
            f"- Found local matches for: `{', '.join(found_years)}`" if found_years else "- Found local matches for: none",
            f"- Missing local matches for: `{', '.join(missing_years)}`" if missing_years else "- Missing local matches for: none",
            "",
            "Files:",
            "- `focus_manifest.csv` lists every focused file with grouping, evidence, and whether it is the preferred copy.",
            "- `source_tracker_crosswalk.csv` maps the workspace's Nevada enrollment-source tracker to local files.",
            "- `mirror/` contains copies of the focused files.",
        ]
    )
    README.write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    print(f"focused_files={len(focus_rows)}")
    print(f"primary_file_families={primary_count}")
    print(f"readme={README}")


if __name__ == "__main__":
    main()
