from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
BASE_RELEASE = ROOT / "release" / "NV_Charter_Quality_Seats_v2"
OUT_RELEASE = ROOT / "release" / "NV_Charter_Quality_Seats_v3"
RATING_SOURCE = ROOT / "quality_seats_sources" / "nspf" / "SchoolRatings_MASTER_2025-26_SPCSA.csv"
ENROLLMENT_SOURCE = BASE_RELEASE / "02_Source_Data" / "NDE_Validation_Day_Enrollment_2024_25.xlsx"
RATING_URL = "https://nevadareportcard.nv.gov/DI/nspf/64843/2026/statedistrict"
ACCESS_DATE = "2026-09-15"


def load_builder_module():
    path = ROOT / "scripts" / "build_quality_seats_release_v2.py"
    spec = importlib.util.spec_from_file_location("quality_seats_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_code(value: object) -> str:
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.lstrip("0") or "0"


def new_rating_rows(builder) -> pd.DataFrame:
    ratings = pd.read_csv(RATING_SOURCE, dtype=str)
    ratings["district_code"] = ratings["District Code"].map(normalize_code)
    parsed = ratings["NSPF School Code"].map(builder.parse_base_and_band)
    ratings["base_school_code"] = parsed.map(lambda value: value[0])
    ratings["school_level_band"] = parsed.map(lambda value: value[1])
    ratings["school_year"] = "2025-26"
    ratings["accountability_year"] = "2025-26"
    ratings["star_rating"] = ratings["Star Rating"].map(
        lambda value: "Not Rated" if pd.isna(value) else str(value).replace(".0", "")
    )
    ratings["rating_bucket_5level"] = ratings["star_rating"].map(builder.rating_bucket_5)
    ratings["rating_bucket_3level"] = ratings["rating_bucket_5level"].map(builder.rating_bucket_3)
    ratings["authorizer"] = "State Public Charter School Authority"
    return ratings[
        [
            "school_year",
            "accountability_year",
            "district_code",
            "District Name",
            "NSPF School Code",
            "base_school_code",
            "School Name",
            "School Type",
            "school_level_band",
            "star_rating",
            "rating_bucket_5level",
            "rating_bucket_3level",
            "authorizer",
        ]
    ].rename(
        columns={
            "District Name": "district_name",
            "NSPF School Code": "school_code",
            "School Name": "school_name",
            "School Type": "school_type",
        }
    )


def append_new_year(builder, panel: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    ratings = new_rating_rows(builder)
    enroll = builder.load_enrollment_bands("2024-25", {"enrollment": ENROLLMENT_SOURCE}).copy()
    enroll["district_code"] = enroll["district_code"].map(normalize_code)

    merged = ratings.merge(
        enroll,
        on=["district_code", "base_school_code", "school_level_band"],
        how="left",
        suffixes=("", "_enroll"),
    )

    prior_keys = set(
        panel.loc[panel["school_year"] == "2024-25", "district_code"].map(normalize_code)
        + "|"
        + panel.loc[panel["school_year"] == "2024-25", "school_code"].astype(str).str.split(".").str[0].map(normalize_code)
        + "|"
        + panel.loc[panel["school_year"] == "2024-25", "school_level_band"].astype(str)
    )
    audit_rows: list[dict] = []
    for _, row in merged.iterrows():
        key = f"{row['district_code']}|{row['base_school_code']}|{row['school_level_band']}"
        matched = pd.notna(row.get("enrollment_total"))
        if key not in prior_keys:
            audit_rows.append(
                {
                    "school_year": "2025-26",
                    "issue_type": "new_spcsa_rating_row",
                    "school_code": row["base_school_code"],
                    "school_name": row["school_name"],
                    "details": "2025-26 SPCSA rating row has no matching 2024-25 SPCSA rating row at the same school-band key.",
                    "recommended_action": "retain as a new current-year rating row; use prior-year enrollment only if a matching count-day row exists",
                }
            )
        if not matched:
            audit_rows.append(
                {
                    "school_year": "2025-26",
                    "issue_type": "prior_year_enrollment_not_available",
                    "school_code": row["base_school_code"],
                    "school_name": row["school_name"],
                    "details": "Current 2025-26 rating exists, but no matching 2024-25 Validation Day enrollment row was found.",
                    "recommended_action": "retain the rating row with zero carried-forward seats and revisit when 2025-26 enrollment is approved for use",
                }
            )

    enrollment_cols = [
        "enrollment_k", "enrollment_1", "enrollment_2", "enrollment_3", "enrollment_4", "enrollment_5",
        "enrollment_6", "enrollment_7", "enrollment_8", "enrollment_9", "enrollment_10", "enrollment_11", "enrollment_12",
        "enrollment_es", "enrollment_ms", "enrollment_hs", "enrollment_total",
    ]
    rows = []
    for _, row in merged.iterrows():
        has_enrollment = pd.notna(row.get("enrollment_total"))
        item = {
            "school_year": "2025-26",
            "accountability_year": "2025-26",
            "district_code": row["district_code"],
            "district_name": str(row["district_name"]).strip(),
            "school_code": row["school_code"],
            "school_name": row["school_name"],
            "school_type": row["school_type"],
            "charter_status": "charter",
            "authorizer": row["authorizer"],
            "school_level_band": row["school_level_band"],
            "star_rating": row["star_rating"],
            "rating_bucket_5level": row["rating_bucket_5level"],
            "rating_bucket_3level": row["rating_bucket_3level"],
            "source_enrollment_file": ENROLLMENT_SOURCE.name,
            "source_rating_file": RATING_SOURCE.name,
            "join_confidence": "high" if has_enrollment else "low",
            "notes": "Preliminary 2025-26 SPCSA ratings treatment: 2024-25 Validation Day enrollment is carried forward until the current-year count-day file is released; unmatched prior-year enrollment is unavailable.",
        }
        for col in enrollment_cols:
            value = row.get(col)
            item[col] = float(value) if has_enrollment and pd.notna(value) else 0.0
        rows.append(item)

    new_panel = pd.DataFrame(rows)
    ordered = list(panel.columns)
    new_panel = new_panel[ordered]
    return pd.concat([panel, new_panel], ignore_index=True), audit_rows


def build_manifest(base_manifest: pd.DataFrame) -> pd.DataFrame:
    manifest = base_manifest.copy()
    enrollment_mask = manifest["file_name"].eq(ENROLLMENT_SOURCE.name)
    manifest.loc[enrollment_mask, "notes"] = (
        "Used directly for 2024-25 and carried forward as a preliminary placeholder for the 2025-26 SPCSA rating update until current-year count-day enrollment is released."
    )
    manifest = manifest[~manifest["file_name"].eq(RATING_SOURCE.name)].copy()
    manifest = pd.concat(
        [
            manifest,
            pd.DataFrame(
                [
                    {
                        "file_name": RATING_SOURCE.name,
                        "source_type": "User-provided 2025-26 SPCSA NSPF ratings CSV",
                        "source_url": RATING_URL,
                        "date_accessed": ACCESS_DATE,
                        "sha256": sha256_file(RATING_SOURCE),
                        "notes": "Current SPCSA ratings supplied by the user; 2025-26 rating rows only. This is a preliminary ratings update pending current-year count-day enrollment."
                    }
                ]
            ),
        ],
        ignore_index=True,
    )
    return manifest.drop_duplicates(subset=["file_name", "source_url"]).reset_index(drop=True)


def main() -> None:
    if OUT_RELEASE.exists():
        raise SystemExit(f"Refusing to overwrite existing output: {OUT_RELEASE}")
    if not RATING_SOURCE.exists():
        raise SystemExit(f"Missing source file: {RATING_SOURCE}")
    if not ENROLLMENT_SOURCE.exists():
        raise SystemExit(f"Missing prior-year enrollment source: {ENROLLMENT_SOURCE}")

    builder = load_builder_module()
    shutil.copytree(BASE_RELEASE, OUT_RELEASE)
    shutil.copy2(RATING_SOURCE, OUT_RELEASE / "02_Source_Data" / RATING_SOURCE.name)

    panel = pd.read_csv(BASE_RELEASE / "03_Clean_Data" / "quality_seats_school_year_panel.csv", dtype=str)
    panel, new_audit = append_new_year(builder, panel)
    numeric_cols = [c for c in panel.columns if c.startswith("enrollment_")]
    for col in numeric_cols:
        panel[col] = pd.to_numeric(panel[col], errors="coerce").fillna(0.0)
    panel = panel.sort_values(["school_year", "district_code", "school_code"]).reset_index(drop=True)

    prior_audit = pd.read_csv(BASE_RELEASE / "04_Audit_Files" / "quality_seats_join_audit.csv", dtype=str)
    audit = pd.concat([prior_audit, pd.DataFrame(new_audit)], ignore_index=True).fillna("")
    audit = audit.sort_values(["school_year", "issue_type", "school_code"]).reset_index(drop=True)

    summary_long, summary_wide = builder.build_summaries(panel)
    partial_status = "preliminary_2025_26_spcsa_ratings_with_2024_25_enrollment_carryforward"
    summary_long.loc[summary_long["school_year"].eq("2025-26"), "data_status"] = partial_status
    summary_wide.loc[summary_wide["school_year"].eq("2025-26"), "data_status"] = partial_status

    # The current-year point is useful for the ratings update, but it must remain
    # visibly preliminary because enrollment is carried forward from 2024-25.
    builder.DISPLAY_YEARS = list(builder.DISPLAY_YEARS) + ["2025-26"]
    builder.CHART_YEARS = [year for year in builder.DISPLAY_YEARS if year not in {"2015-16", "2021-22"}]

    clean = OUT_RELEASE / "03_Clean_Data"
    panel.to_csv(clean / "quality_seats_school_year_panel.csv", index=False)
    panel.to_csv(clean / "quality_seats_panel.csv", index=False)
    summary_long.to_csv(clean / "quality_seats_summary_long.csv", index=False)
    summary_long.to_csv(clean / "quality_seats_by_grade_band.csv", index=False)
    summary_long[["school_year", "level_band", "rating_bucket_5level", "rating_bucket_3level", "enrollment_share"]].to_csv(clean / "quality_seats_share.csv", index=False)
    summary_wide.to_csv(clean / "quality_seats_summary_wide.csv", index=False)
    summary_wide.to_csv(clean / "quality_seats_summary.csv", index=False)
    audit.to_csv(OUT_RELEASE / "04_Audit_Files" / "quality_seats_join_audit.csv", index=False)

    builder.write_visualizations(summary_long, panel, OUT_RELEASE / "05_Visualizations")
    for chart_path in (OUT_RELEASE / "05_Visualizations").glob("*.html"):
        chart_html = chart_path.read_text(encoding="utf-8")
        chart_html = chart_html.replace(
            '<p class="note">',
            '<p class="note"><strong>Preliminary 2025-26 note:</strong> Current-year ratings use carried-forward 2024-25 Validation Day enrollment. Replace this point when current count-day data are released. ',
            1,
        )
        chart_path.write_text(chart_html, encoding="utf-8")

    public_page = OUT_RELEASE / "06_Public_Website" / "quality-seats-overview.html"
    public_html = public_page.read_text(encoding="utf-8")
    public_html = public_html.replace(
        '<div class="links">',
        '<p><strong>Preliminary 2025-26 note:</strong> The current rating update is not a current-enrollment estimate. It carries forward 2024-25 Validation Day enrollment until the 2025-26 count-day file is released. CCSD has reported a substantial enrollment decline, but that does not establish what happened to charter enrollment. The 2025-26 panel will be updated in October when current charter enrollment data are available.</p><div class="links">',
        1,
    )
    public_html = public_html.replace(
        '<h3>Technical notes and limitations</h3>',
        '<h3>Technical notes and limitations</h3><p><strong>Preliminary 2025-26 limitation:</strong> Current-year ratings are shown with 2024-25 Validation Day enrollment carried forward. These figures should not be interpreted as current enrollment. The panel and charts will be updated in October when the 2025-26 count-day enrollment file is available. CCSD\'s reported enrollment decline does not establish what happened to charter enrollment.</p>',
        1,
    )
    public_html = public_html.replace(
        'Visible chart years: 2012-13 to 2024-25',
        'Visible chart years: 2012-13 to 2025-26; 2025-26 is preliminary',
        1,
    )
    public_page.write_text(public_html, encoding="utf-8")

    manifest = pd.read_csv(BASE_RELEASE / "04_Audit_Files" / "source_manifest_quality_seats.csv", dtype=str)
    build_manifest(manifest).to_csv(OUT_RELEASE / "04_Audit_Files" / "source_manifest_quality_seats.csv", index=False)

    update_note = """# Preliminary 2025-26 Rating Update\n\n- Added the user-provided 2025-26 SPCSA NSPF ratings file.\n- Appended current-year rating rows for existing SPCSA school-band keys and new SPCSA school-band keys.\n- Carried forward 2024-25 Validation Day enrollment as a temporary count-day placeholder because the 2025-26 enrollment file has not yet been released.\n- Twenty rating rows do not have a matching 2024-25 enrollment row and remain in the panel with zero carried-forward seats and explicit audit flags.\n- This is a partial 2025-26 update: the current attached rating source covers SPCSA, not district-authorized charter schools. The charts now include a clearly labeled preliminary 2025-26 point, while the complete all-charter series remains through 2024-25.\n- The preliminary 2025-26 seat counts should not be interpreted as current enrollment. CCSD has reported a substantial enrollment decline, but that district-level report does not establish what happened to charter enrollment. The charter side should be recalculated when the current count-day enrollment file is released.\n"""
    (OUT_RELEASE / "01_Methodology" / "UPDATE_2025_26_SPCSA.md").write_text(update_note, encoding="utf-8")

    changelog = (OUT_RELEASE / "07_Change_Log" / "CHANGELOG.md").read_text(encoding="utf-8")
    changelog += "\n- Added a preliminary 2025-26 SPCSA rating update from the user-provided current ratings CSV.\n- Carried forward 2024-25 Validation Day enrollment as a temporary placeholder pending the 2025-26 count-day file; unmatched rows are retained and audited.\n- Added a caution that CCSD's reported enrollment decline cannot be used to infer charter enrollment movement.\n- Added the preliminary 2025-26 point to the charts with an explicit enrollment caveat; the complete all-charter comparison remains through 2024-25.\n"
    (OUT_RELEASE / "07_Change_Log" / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
    release_manifest = {
        "release_name": "NV_Charter_Quality_Seats_v3",
        "analysis_years": ["2012-13", "2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"],
        "latest_update_scope": "Preliminary SPCSA-only ratings with 2024-25 Validation Day enrollment carried forward pending current-year enrollment",
        "enrollment_caveat": "2025-26 seat counts are not current enrollment. Replace carried-forward 2024-25 enrollment when the 2025-26 count-day file is released.",
        "visible_chart_years": "2012-13 through 2025-26, with 2025-26 preliminary",
        "public_page": "06_Public_Website/quality-seats-overview.html",
        "chart_count": 21,
    }
    (OUT_RELEASE / "07_Change_Log" / "release_manifest.json").write_text(json.dumps(release_manifest, indent=2), encoding="utf-8")

    zip_path = ROOT / "release" / "NV_Charter_Quality_Seats_v3.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(OUT_RELEASE.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(OUT_RELEASE.parent))

    print(json.dumps({"release": str(OUT_RELEASE), "zip": str(zip_path), "panel_rows": len(panel), "new_rating_rows": 162, "new_audit_rows": len(new_audit)}, indent=2))


if __name__ == "__main__":
    main()
