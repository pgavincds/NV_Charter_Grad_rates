from __future__ import annotations

import hashlib
import json
import math
import shutil
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "quality_seats_sources"
LEGACY_DIR = SOURCE_DIR / "legacy"
HANDOFF_DIR = ROOT / "handoff_package_v3" / "codex_handoff_quality_seats_and_grad_v3"
RELEASE_ROOT = ROOT / "release" / "NV_Charter_Quality_Seats_v2"
PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.35.2.min.js"


ANALYSIS_YEARS = {
    "2015-16": {
        "column_year": 2016,
        "ratings": SOURCE_DIR / "nspf_merged" / "SchoolRatings_MASTER_2015-16.csv",
        "enrollment": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2015_16.xlsx",
        "source_rating_url": "https://nevadareportcard.nv.gov/DI/nspf/<district_id>/2016/statedistrict",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2015_2016_SY_Student_Counts_a632177572.xlsx",
    },
    "2016-17": {
        "column_year": 2017,
        "ratings": SOURCE_DIR / "nspf_merged" / "SchoolRatings_MASTER_2016-17.csv",
        "enrollment": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2016_17.xlsx",
        "source_rating_url": "https://nevadareportcard.nv.gov/DI/nspf/<district_id>/2017/statedistrict",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20162017_Oct1_Enrol_Num_1a5ef511e2.xlsx",
    },
    "2017-18": {
        "column_year": 2018,
        "ratings": SOURCE_DIR / "nspf_merged" / "SchoolRatings_MASTER_2017-18.csv",
        "enrollment": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2017_18.xlsx",
        "source_rating_url": "https://nevadareportcard.nv.gov/DI/nspf/<district_id>/2018/statedistrict",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20172018_Numberofstudents_c45aa90c9a.xlsx",
    },
    "2018-19": {
        "column_year": 2019,
        "ratings": SOURCE_DIR / "nspf_merged" / "SchoolRatings_MASTER_2018-19.csv",
        "enrollment": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2018_19.xlsx",
        "source_rating_url": "https://nevadareportcard.nv.gov/DI/nspf/<district_id>/2019/statedistrict",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20182019_Numberof_Student102018_1ea97446e0.xlsx",
    },
    "2019-20": {
        "column_year": 2020,
        "ratings": SOURCE_DIR / "nspf_merged" / "SchoolRatings_MASTER_2019-20.csv",
        "enrollment": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2019_20.xlsx",
        "source_rating_url": "https://nevadareportcard.nv.gov/DI/nspf/<district_id>/2020/statedistrict",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20192020_Numberof_Student11142019_651a96a7a8.xlsx",
    },
    "2020-21": {
        "column_year": 2021,
        "ratings": SOURCE_DIR / "nspf_merged" / "SchoolRatings_MASTER_2020-21.csv",
        "enrollment": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2020_21.xlsx",
        "source_rating_url": "https://nevadareportcard.nv.gov/DI/nspf/<district_id>/2021/statedistrict",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2020_2021_School_Year_Numberof_Students_f703bba063.xlsx",
    },
    "2021-22": {
        "column_year": 2022,
        "ratings": SOURCE_DIR / "nspf_merged" / "SchoolRatings_MASTER_2021-22.csv",
        "enrollment": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2021_22.xlsx",
        "source_rating_url": "https://nevadareportcard.nv.gov/DI/nspf/<district_id>/2022/statedistrict",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2021_2022schoolyearcounts1021_0199ab6d3b.xlsx",
    },
    "2022-23": {
        "column_year": 2023,
        "ratings": SOURCE_DIR / "nspf" / "SchoolRatings_MASTER_2022-23.csv",
        "enrollment": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2022_23.xlsx",
        "source_rating_url": "https://raw.githubusercontent.com/pgavincds/nevada-nspf-toolkit/main/data/2022-23/SchoolRatings_MASTER_2022-23.csv",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2022_2023_enrollment_numbers_2224fa62e5.xlsx",
    },
    "2023-24": {
        "column_year": 2024,
        "ratings": SOURCE_DIR / "nspf" / "SchoolRatings_MASTER_2023-24.csv",
        "enrollment": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2023_24.xlsx",
        "source_rating_url": "https://raw.githubusercontent.com/pgavincds/nevada-nspf-toolkit/main/data/2023-24/SchoolRatings_MASTER_2023-24.csv",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2023_2024_school_year_validation_day_student_counts_2e68b10570.xlsx",
    },
    "2024-25": {
        "column_year": 2025,
        "ratings": SOURCE_DIR / "nspf" / "SchoolRatings_MASTER_2024-25.csv",
        "enrollment": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2024_25.xlsx",
        "source_rating_url": "https://raw.githubusercontent.com/pgavincds/nevada-nspf-toolkit/main/data/2024-25/SchoolRatings_MASTER_2024-25.csv",
        "source_enrollment_url": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2024_2025_school_year_validation_day_student_counts_16036836ca.xlsx",
    },
}

ARCHIVED_ENROLLMENT_FILES = {
    "2015-16": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2015_16.xlsx",
    "2016-17": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2016_17.xlsx",
    "2017-18": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2017_18.xlsx",
    "2018-19": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2018_19.xlsx",
    "2019-20": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2019_20.xlsx",
    "2020-21": SOURCE_DIR / "enrollment" / "NDE_Validation_Day_Enrollment_2020_21.xlsx",
    "2021-22": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2021_22.xlsx",
    "2022-23": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2022_23.xlsx",
    "2023-24": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2023_24.xlsx",
    "2024-25": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2024_25.xlsx",
    "2025-26": HANDOFF_DIR / "01_ATTACHED_EVIDENCE" / "Validation_Day_enrollment" / "NDE_Validation_Day_Enrollment_2025_26_suppressed.xlsx",
}

ENROLLMENT_URLS = {
    "2015-16": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2015_2016_SY_Student_Counts_a632177572.xlsx",
    "2016-17": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20162017_Oct1_Enrol_Num_1a5ef511e2.xlsx",
    "2017-18": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20172018_Numberofstudents_c45aa90c9a.xlsx",
    "2018-19": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20182019_Numberof_Student102018_1ea97446e0.xlsx",
    "2019-20": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/20192020_Numberof_Student11142019_651a96a7a8.xlsx",
    "2020-21": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2020_2021_School_Year_Numberof_Students_f703bba063.xlsx",
    "2021-22": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2021_2022schoolyearcounts1021_0199ab6d3b.xlsx",
    "2022-23": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2022_2023_enrollment_numbers_2224fa62e5.xlsx",
    "2023-24": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2023_2024_school_year_validation_day_student_counts_2e68b10570.xlsx",
    "2024-25": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/2024_2025_school_year_validation_day_student_counts_16036836ca.xlsx",
    "2025-26": "https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/suppressed_2025_2026_school_year_enrollment_counts_for_website_11_03_25_c9f4d44d51.xlsx",
}

LEVEL_ORDER = ["ES", "MS", "HS"]
RATING_ORDER_5 = ["1", "2", "3", "4", "5", "Not Rated"]
RATING_ORDER_3 = ["1-2", "3", "4-5", "Not Rated"]
DISPLAY_YEARS = ["2012-13", "2013-14", "2014-15"] + list(ANALYSIS_YEARS.keys())
CHART_YEARS = [y for y in DISPLAY_YEARS if y not in {"2015-16", "2021-22"}]
LEGACY_PANEL_FILE = LEGACY_DIR / "legacy_state_charters_estimated_panel_2012_13_to_2014_15.csv"
LEGACY_TOTALS_FILE = LEGACY_DIR / "legacy_state_charters_school_totals_2012_13_to_2014_15.csv"
LEGACY_AUDIT_FILE = LEGACY_DIR / "legacy_state_charters_estimation_audit_2012_13_to_2014_15.csv"
LEGACY_2015_SHEETS = {
    "State Public Charter School Authority": "SPCSA",
    "Clark County School District": "CCSD",
    "Washoe County School District": "WCSD",
    "Carson City School District": "Carson City",
}
PAUSE_STATUS = {
    "2012-13": "legacy_pdf_estimated_band_splits",
    "2013-14": "legacy_pdf_estimated_band_splits",
    "2014-15": "legacy_pdf_estimated_band_splits",
    "2015-16": "initial_transition_not_shown",
    "2016-17": "first_stable_baseline",
    "2017-18": "standard_reporting",
    "2018-19": "standard_reporting",
    "2019-20": "pandemic_disruption",
    "2020-21": "pandemic_irregular",
    "2021-22": "testing_recovery_not_rated",
    "2022-23": "modern_reporting",
    "2023-24": "modern_reporting",
    "2024-25": "modern_reporting",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dirs() -> dict[str, Path]:
    dirs = {
        "method": RELEASE_ROOT / "01_Methodology",
        "source": RELEASE_ROOT / "02_Source_Data",
        "clean": RELEASE_ROOT / "03_Clean_Data",
        "audit": RELEASE_ROOT / "04_Audit_Files",
        "viz": RELEASE_ROOT / "05_Visualizations",
        "web": RELEASE_ROOT / "06_Public_Website",
        "log": RELEASE_ROOT / "07_Change_Log",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def parse_base_and_band(code: str) -> tuple[str, str]:
    text = str(code).strip()
    if "." in text:
        base, suffix = text.split(".", 1)
    else:
        base, suffix = text, ""
    base = base.lstrip("0") or "0"
    band = {"1": "ES", "2": "MS", "3": "HS"}.get(suffix.strip(), "Other")
    return base, band


def normalize_grade(value: object) -> str | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip().upper().replace("GRADE_", "")
    mapping = {"0K": "K", "KG": "K", "K": "K", "PK": "PK", "PRE-K": "PK"}
    if text in mapping:
        return mapping[text]
    if text.isdigit():
        return str(int(text))
    return None


def band_for_grade(grade: str) -> str | None:
    if grade in {"K", "1", "2", "3", "4", "5"}:
        return "ES"
    if grade in {"6", "7", "8"}:
        return "MS"
    if grade in {"9", "10", "11", "12"}:
        return "HS"
    return None


def rating_bucket_5(star_rating: object) -> str:
    if pd.isna(star_rating):
        return "Not Rated"
    text = str(star_rating).strip()
    if text in {"-1", "Not Rated", ""}:
        return "Not Rated"
    if text.endswith(".0"):
        text = text[:-2]
    if text in {"1", "2", "3", "4", "5"}:
        return text
    return "Not Rated"


def rating_bucket_3(bucket_5: str) -> str:
    if bucket_5 in {"1", "2"}:
        return "1-2"
    if bucket_5 == "3":
        return "3"
    if bucket_5 in {"4", "5"}:
        return "4-5"
    return "Not Rated"


def is_charter_school_type(year_label: str, school_type: str, district_code: str = "", district_name: str = "") -> bool:
    text = str(school_type or "").strip()
    dc = str(district_code).replace(".0", "").strip()
    dn = str(district_name or "").strip()
    is_spcsa = dc == "18" or "SPCSA" in dn or "State Public Charter" in dn
    if year_label in {"2020-21", "2021-22", "2022-23", "2023-24", "2024-25"}:
        return text in {"SPCSA", "District Charter"}
    if year_label in {"2019-20"}:
        return text in {"Charter District", "Charter SPCSA"}
    if year_label in {"2017-18", "2018-19"}:
        if is_spcsa:
            return text in {"Charter SPCSA", "Charter SPCSA Virtual", "Zoom SPCSA"}
        return text in {"Charter District", "Victory District Charter", "Zoom District Charter"}
    if year_label in {"2015-16", "2016-17"}:
        if year_label == "2016-17" and is_spcsa:
            return text in {"Charter", "Charter Virtual School", "Regular"}
        return text in {"Charter", "Charter Virtual School"}
    return False


def authorizer_from_row(district_code: str, district_name: str) -> str:
    dc = str(district_code).replace(".0", "").strip()
    dn = str(district_name).strip()
    if dc == "18" or "SPCSA" in dn or "State Public Charter" in dn:
        return "State Public Charter School Authority"
    if dc == "2" or dn == "Clark":
        return "Clark County School District"
    if dc == "16" or dn == "Washoe":
        return "Washoe County School District"
    if dc == "13" or "Carson" in dn:
        return "Carson City School District"
    if "Achievement" in dn:
        return "Achievement School District"
    return dn


def load_rating_rows(year_label: str, info: dict) -> pd.DataFrame:
    df = pd.read_csv(info["ratings"], dtype=str)
    df = df[
        df.apply(
            lambda row: is_charter_school_type(
                year_label,
                row.get("School Type", ""),
                row.get("District Code", ""),
                row.get("District Name", ""),
            ),
            axis=1,
        )
    ].copy()
    df["District Code"] = df["District Code"].astype(str).str.replace(r"\.0$", "", regex=True)
    parsed = df["NSPF School Code"].map(parse_base_and_band)
    df["base_school_code"] = [p[0] for p in parsed]
    df["school_level_band"] = [p[1] for p in parsed]
    df["school_year"] = year_label
    df["accountability_year"] = year_label
    df["star_rating"] = df["Star Rating"].map(lambda x: "Not Rated" if pd.isna(x) else str(x).replace(".0", ""))
    df["rating_bucket_5level"] = df["star_rating"].map(rating_bucket_5)
    df["rating_bucket_3level"] = df["rating_bucket_5level"].map(rating_bucket_3)
    df["authorizer"] = [authorizer_from_row(dc, dn) for dc, dn in zip(df["District Code"], df["District Name"])]
    return df[
        ["school_year", "accountability_year", "District Code", "District Name", "NSPF School Code", "base_school_code", "School Name", "School Type", "school_level_band", "star_rating", "rating_bucket_5level", "rating_bucket_3level", "authorizer"]
    ].rename(
        columns={
            "District Code": "district_code",
            "District Name": "district_name",
            "NSPF School Code": "school_code",
            "School Name": "school_name",
            "School Type": "school_type",
        }
    )


def detect_header_df(path: Path, sheet_name: str, required_cols: set[str]) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=sheet_name, header=None, dtype=object)
    header_idx = None
    for i in range(min(len(raw), 25)):
        vals = {str(v).strip() for v in raw.iloc[i].tolist() if pd.notna(v)}
        if required_cols.issubset(vals):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"Could not detect header row in {path.name} / {sheet_name}")
    header = [str(v).strip() if pd.notna(v) else f"col_{j}" for j, v in enumerate(raw.iloc[header_idx].tolist())]
    df = raw.iloc[header_idx + 1 :].copy()
    df.columns = header
    df = df.dropna(how="all")
    return df


def parse_2015_16_enrollment(path: Path) -> pd.DataFrame:
    rows = []
    for authorizer, sheet in LEGACY_2015_SHEETS.items():
        raw = pd.read_excel(path, sheet_name=sheet, header=None, dtype=object)
        current = None
        for _, r in raw.iterrows():
            a = r.iloc[0] if len(r) > 0 else None
            b = r.iloc[1] if len(r) > 1 else None
            c = r.iloc[2] if len(r) > 2 else None
            if pd.notna(a) and str(a).strip().isdigit() and pd.notna(b):
                code = str(a).strip()
                name = str(b).strip()
                total = c
                current = {
                    "district_name": authorizer,
                    "school_code": code,
                    "school_name": name,
                    "grades": {},
                }
                rows.append(current)
                continue
            if current is not None and pd.notna(b) and str(b).startswith("Grade:"):
                grade = normalize_grade(str(b).split(":", 1)[1].strip())
                if grade:
                    current["grades"][grade] = c
    out = []
    for row in rows:
        rec = {
            "district_name": row["district_name"],
            "school_code": row["school_code"],
            "school_name": row["school_name"],
        }
        for grade in ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
            rec[f"enrollment_{grade.lower() if grade != 'K' else 'k'}"] = to_number(row["grades"].get(grade, 0))
        out.append(rec)
    return pd.DataFrame(out)


def parse_school_totals_with_grade_cols(path: Path, sheet_name: str) -> pd.DataFrame:
    df = detect_header_df(path, sheet_name, {"School Code", "School Name"})
    recs = []
    for _, row in df.iterrows():
        rec = {
            "district_name": row.get("District") or row.get("Local Education Agency Name") or row.get("Master District Name"),
            "district_code": row.get("District Code") or row.get("Local Education Agency Code") or row.get("Master District Code"),
            "school_code": row.get("School Code"),
            "school_name": row.get("School Name"),
        }
        for grade in ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
            source_col = f"Grade_{grade if grade != 'K' else 'K'}"
            rec[f"enrollment_{grade.lower() if grade != 'K' else 'k'}"] = to_number(row.get(source_col))
        recs.append(rec)
    return pd.DataFrame(recs)


def parse_grade_detail_sheet(path: Path) -> pd.DataFrame:
    xls = pd.ExcelFile(path)
    candidates = [
        s
        for s in xls.sheet_names
        if "School Grade Subgroups Data" in s or "School Grade Details" in s or "Schools by Grade and Ethnicity" in s
    ]
    if not candidates:
        raise ValueError(f"No grade detail sheet in {path}")
    df = detect_header_df(path, candidates[0], {"School Code", "School Name"})
    rename = {}
    for col in df.columns:
        text = str(col).strip()
        if text in {"Local Education Agency Code", "District Code"}:
            rename[col] = "district_code"
        elif text in {"Local Education Agency Name", "District", "District Name"}:
            rename[col] = "district_name"
        elif text == "Master District Code":
            rename[col] = "district_code"
        elif text == "Master District Name":
            rename[col] = "district_name"
        elif text == "School Code":
            rename[col] = "school_code"
        elif text == "School Name":
            rename[col] = "school_name"
        elif text in {"Grade", "Grade Level"}:
            rename[col] = "grade"
        elif text == "Total":
            rename[col] = "total"
    df = df.rename(columns=rename)
    for target in ["district_code", "district_name", "school_code", "school_name", "grade", "total"]:
        matching = [c for c in df.columns if c == target]
        if len(matching) > 1:
            combined = df.loc[:, matching].bfill(axis=1).iloc[:, 0]
            df = df.drop(columns=matching)
            df[target] = combined
    df = df[["district_code", "district_name", "school_code", "school_name", "grade", "total"]].copy()
    df["grade_norm"] = df["grade"].map(normalize_grade)
    df = df[df["grade_norm"].notna()].copy()
    pivot = (
        df.assign(total_num=df["total"].map(to_number))
        .pivot_table(index=["district_code", "district_name", "school_code", "school_name"], columns="grade_norm", values="total_num", aggfunc="sum", fill_value=0)
        .reset_index()
    )
    recs = []
    for _, row in pivot.iterrows():
        rec = {
            "district_code": row["district_code"],
            "district_name": row["district_name"],
            "school_code": row["school_code"],
            "school_name": row["school_name"],
        }
        for grade in ["K", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
            rec[f"enrollment_{grade.lower() if grade != 'K' else 'k'}"] = float(row.get(grade, 0) or 0)
        recs.append(rec)
    return pd.DataFrame(recs)


def load_enrollment_base(year_label: str, path: Path) -> pd.DataFrame:
    if year_label == "2015-16":
        return parse_2015_16_enrollment(path)
    if year_label == "2016-17":
        return parse_school_totals_with_grade_cols(path, "School Totals")
    return parse_grade_detail_sheet(path)


def to_number(value: object) -> float:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return 0.0
    text = str(value).strip()
    if text in {"", "*", "**", "***", "nan", "N/A", "n/a"}:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def load_enrollment_bands(year_label: str, info: dict) -> pd.DataFrame:
    base = load_enrollment_base(year_label, info["enrollment"]).copy()
    for col in [c for c in base.columns if c.startswith("enrollment_")]:
        base[col] = base[col].map(to_number)
    if "district_code" not in base.columns:
        base["district_code"] = "0"
    base["district_code"] = base["district_code"].astype(str).str.replace(r"\.0$", "", regex=True).str.lstrip("0").replace("", "0")
    base["base_school_code"] = base["school_code"].astype(str).str.replace(r"\.0$", "", regex=True).str.lstrip("0").replace("", "0")

    band_rows = []
    for _, row in base.iterrows():
        es = sum(row.get(f"enrollment_{g}", 0) for g in ["k", "1", "2", "3", "4", "5"])
        ms = sum(row.get(f"enrollment_{g}", 0) for g in ["6", "7", "8"])
        hs = sum(row.get(f"enrollment_{g}", 0) for g in ["9", "10", "11", "12"])
        for band, total in [("ES", es), ("MS", ms), ("HS", hs)]:
            if total > 0:
                band_rows.append(
                    {
                        "school_year": year_label,
                        "base_school_code": row["base_school_code"],
                        "district_code": row["district_code"],
                        "district_name": row.get("district_name", ""),
                        "school_name": row["school_name"],
                        "school_level_band": band,
                        "enrollment_total": total,
                        "enrollment_es": es,
                        "enrollment_ms": ms,
                        "enrollment_hs": hs,
                        "enrollment_k": row.get("enrollment_k", 0),
                        "enrollment_1": row.get("enrollment_1", 0),
                        "enrollment_2": row.get("enrollment_2", 0),
                        "enrollment_3": row.get("enrollment_3", 0),
                        "enrollment_4": row.get("enrollment_4", 0),
                        "enrollment_5": row.get("enrollment_5", 0),
                        "enrollment_6": row.get("enrollment_6", 0),
                        "enrollment_7": row.get("enrollment_7", 0),
                        "enrollment_8": row.get("enrollment_8", 0),
                        "enrollment_9": row.get("enrollment_9", 0),
                        "enrollment_10": row.get("enrollment_10", 0),
                        "enrollment_11": row.get("enrollment_11", 0),
                        "enrollment_12": row.get("enrollment_12", 0),
                    }
                )
    return pd.DataFrame(band_rows)


def build_quality_panel() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    panel_rows = []
    audit_rows = []
    source_rows = []
    for year_label, info in ANALYSIS_YEARS.items():
        ratings = load_rating_rows(year_label, info)
        enroll = load_enrollment_bands(year_label, info)

        merged = ratings.merge(
            enroll,
            on=["school_year", "base_school_code", "school_level_band"],
            how="left",
            suffixes=("", "_enroll"),
        )
        matched_keys = set(
            tuple(x)
            for x in merged[merged["enrollment_total"].notna()][["base_school_code", "school_level_band"]].drop_duplicates().itertuples(index=False, name=None)
        )
        for _, row in merged[merged["enrollment_total"].isna()].iterrows():
            audit_rows.append(
                {
                    "school_year": year_label,
                    "issue_type": "published_rating_row_needs_manual_review",
                    "school_code": row["base_school_code"],
                    "school_name": row["school_name"],
                    "details": f"Published charter rating row exists for band {row['school_level_band']}, but no usable same-band enrollment record was recovered. This often indicates a school that was too new, too small, or otherwise not fully rated in practice.",
                    "recommended_action": "hold for later manual review; do not force a seat count into the published series",
                }
            )
        rating_bases = set(ratings["base_school_code"])
        rating_band_map = ratings.groupby("base_school_code")["school_level_band"].agg(lambda s: sorted(set(s))).to_dict()
        for _, row in enroll.iterrows():
            key = (row["base_school_code"], row["school_level_band"])
            if row["base_school_code"] in rating_bases and key not in matched_keys:
                published_bands = rating_band_map.get(row["base_school_code"], [])
                if published_bands:
                    audit_rows.append(
                        {
                            "school_year": year_label,
                            "issue_type": "off_band_enrollment_excluded",
                            "school_code": row["base_school_code"],
                            "school_name": row["school_name"],
                            "details": f"Enrollment exists for band {row['school_level_band']}, but the published charter rating row(s) only exist for {', '.join(published_bands)}. Off-band spillover grades are excluded under the suffix-based ES/MS/HS standard.",
                            "recommended_action": "no action unless manually overriding the statewide suffix-based band standard",
                        }
                    )
                    continue
                audit_rows.append(
                    {
                        "school_year": year_label,
                        "issue_type": "unmatched_enrollment_band",
                        "school_code": row["base_school_code"],
                        "school_name": row["school_name"],
                        "details": f"Enrollment exists for band {row['school_level_band']} but no charter rating row matched.",
                        "recommended_action": "inspect whether school lacks a published rating band row",
                    }
                )

        for _, row in merged.iterrows():
            panel_rows.append(
                {
                    "school_year": year_label,
                    "accountability_year": row["accountability_year"],
                    "district_code": row["district_code"],
                    "district_name": row["district_name"],
                    "school_code": row["school_code"],
                    "school_name": row["school_name"],
                    "school_type": row["school_type"],
                    "charter_status": "charter",
                    "authorizer": row["authorizer"],
                    "school_level_band": row["school_level_band"],
                    "star_rating": row["star_rating"],
                    "rating_bucket_5level": row["rating_bucket_5level"],
                    "rating_bucket_3level": row["rating_bucket_3level"],
                    "enrollment_k": row.get("enrollment_k", 0) if pd.notna(row.get("enrollment_k", 0)) else 0,
                    "enrollment_1": row.get("enrollment_1", 0) if pd.notna(row.get("enrollment_1", 0)) else 0,
                    "enrollment_2": row.get("enrollment_2", 0) if pd.notna(row.get("enrollment_2", 0)) else 0,
                    "enrollment_3": row.get("enrollment_3", 0) if pd.notna(row.get("enrollment_3", 0)) else 0,
                    "enrollment_4": row.get("enrollment_4", 0) if pd.notna(row.get("enrollment_4", 0)) else 0,
                    "enrollment_5": row.get("enrollment_5", 0) if pd.notna(row.get("enrollment_5", 0)) else 0,
                    "enrollment_6": row.get("enrollment_6", 0) if pd.notna(row.get("enrollment_6", 0)) else 0,
                    "enrollment_7": row.get("enrollment_7", 0) if pd.notna(row.get("enrollment_7", 0)) else 0,
                    "enrollment_8": row.get("enrollment_8", 0) if pd.notna(row.get("enrollment_8", 0)) else 0,
                    "enrollment_9": row.get("enrollment_9", 0) if pd.notna(row.get("enrollment_9", 0)) else 0,
                    "enrollment_10": row.get("enrollment_10", 0) if pd.notna(row.get("enrollment_10", 0)) else 0,
                    "enrollment_11": row.get("enrollment_11", 0) if pd.notna(row.get("enrollment_11", 0)) else 0,
                    "enrollment_12": row.get("enrollment_12", 0) if pd.notna(row.get("enrollment_12", 0)) else 0,
                    "enrollment_es": row.get("enrollment_es", 0) if pd.notna(row.get("enrollment_es", 0)) else 0,
                    "enrollment_ms": row.get("enrollment_ms", 0) if pd.notna(row.get("enrollment_ms", 0)) else 0,
                    "enrollment_hs": row.get("enrollment_hs", 0) if pd.notna(row.get("enrollment_hs", 0)) else 0,
                    "enrollment_total": row.get("enrollment_total", 0) if pd.notna(row.get("enrollment_total", 0)) else 0,
                    "source_enrollment_file": Path(info["enrollment"]).name,
                    "source_rating_file": Path(info["ratings"]).name,
                    "join_confidence": "high" if pd.notna(row.get("enrollment_total")) else "low",
                    "notes": PAUSE_STATUS.get(year_label, ""),
                }
            )

        source_rows.append(
            {
                "file_name": Path(info["ratings"]).name,
                "source_type": "NSPF ratings master CSV",
                "source_url": info["source_rating_url"],
                "date_accessed": "2026-06-06",
                "sha256": sha256_file(Path(info["ratings"])),
                "notes": f"Used directly in historical quality seats joins for {year_label}.",
            }
        )
        source_rows.append(
            {
                "file_name": Path(info["enrollment"]).name,
                "source_type": "NDE Validation Day enrollment workbook",
                "source_url": info["source_enrollment_url"],
                "date_accessed": "2026-06-06",
                "sha256": sha256_file(Path(info["enrollment"])),
                "notes": f"Used directly in historical quality seats joins for {year_label}.",
            }
        )

    for year_label, path in ARCHIVED_ENROLLMENT_FILES.items():
        if year_label not in ANALYSIS_YEARS:
            source_rows.append(
                {
                    "file_name": path.name,
                    "source_type": "NDE Validation Day enrollment workbook",
                    "source_url": ENROLLMENT_URLS[year_label],
                    "date_accessed": "2026-06-06",
                    "sha256": sha256_file(path),
                    "notes": "Archived for future extension.",
                }
            )

    if LEGACY_PANEL_FILE.exists():
        legacy_panel = pd.read_csv(LEGACY_PANEL_FILE)
        legacy_panel = legacy_panel.drop(
            columns=[
                c
                for c in [
                    "legacy_school_total_enrollment",
                    "legacy_band_share_reference_year",
                    "legacy_band_share_used",
                ]
                if c in legacy_panel.columns
            ]
        )
        panel_rows.extend(legacy_panel.to_dict("records"))
        source_rows.append(
            {
                "file_name": LEGACY_PANEL_FILE.name,
                "source_type": "Legacy estimated charter panel CSV",
                "source_url": "local_reconstruction_from_legacy_state_charter_pdfs",
                "date_accessed": "2026-06-07",
                "sha256": sha256_file(LEGACY_PANEL_FILE),
                "notes": "Legacy 2012-13 through 2014-15 state-charter band estimates built from recovered PDF school totals and mapped NSPF band rows.",
            }
        )
    if LEGACY_TOTALS_FILE.exists():
        source_rows.append(
            {
                "file_name": LEGACY_TOTALS_FILE.name,
                "source_type": "Legacy state-charter school totals CSV",
                "source_url": "derived_from_legacy_state_charter_accountability_pdfs",
                "date_accessed": "2026-06-07",
                "sha256": sha256_file(LEGACY_TOTALS_FILE),
                "notes": "School-level total enrollment recovered from 2012-13 through 2014-15 state-charter accountability PDFs.",
            }
        )
    if LEGACY_AUDIT_FILE.exists():
        legacy_audit = pd.read_csv(LEGACY_AUDIT_FILE)
        audit_rows.extend(legacy_audit.to_dict("records"))
    return pd.DataFrame(panel_rows), pd.DataFrame(audit_rows), pd.DataFrame(source_rows)


def build_summaries(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for (year, level), sub in panel.groupby(["school_year", "school_level_band"]):
        denom = sub["enrollment_total"].sum()
        for bucket in RATING_ORDER_5:
            ss = sub[sub["rating_bucket_5level"] == bucket]
            rows.append(
                {
                    "school_year": year,
                    "level_band": level,
                    "rating_bucket_5level": bucket,
                    "rating_bucket_3level": rating_bucket_3(bucket),
                    "enrollment": ss["enrollment_total"].sum(),
                    "enrollment_share": (ss["enrollment_total"].sum() / denom) if denom else 0,
                    "school_count": len(ss),
                }
            )
        for bucket in RATING_ORDER_3:
            ss = sub[sub["rating_bucket_3level"] == bucket]
            rows.append(
                {
                    "school_year": year,
                    "level_band": level,
                    "rating_bucket_5level": "Collapsed",
                    "rating_bucket_3level": bucket,
                    "enrollment": ss["enrollment_total"].sum(),
                    "enrollment_share": (ss["enrollment_total"].sum() / denom) if denom else 0,
                    "school_count": len(ss),
                }
            )
    long_df = pd.DataFrame(rows)
    wide_5 = long_df[long_df["rating_bucket_5level"] != "Collapsed"].pivot_table(
        index=["school_year", "level_band"], columns="rating_bucket_5level", values=["enrollment", "enrollment_share", "school_count"], aggfunc="first", fill_value=0
    )
    wide_3 = long_df[long_df["rating_bucket_5level"] == "Collapsed"].pivot_table(
        index=["school_year", "level_band"], columns="rating_bucket_3level", values=["enrollment", "enrollment_share", "school_count"], aggfunc="first", fill_value=0
    )
    wide_5.columns = [f"fivelevel_{a}_{b}" for a, b in wide_5.columns]
    wide_3.columns = [f"collapsed_{a}_{b}" for a, b in wide_3.columns]
    wide = pd.concat([wide_5, wide_3], axis=1).reset_index()
    long_df["data_status"] = long_df["school_year"].map(PAUSE_STATUS).fillna("standard_reporting")
    wide["data_status"] = wide["school_year"].map(PAUSE_STATUS).fillna("standard_reporting")
    return long_df, wide


def plotly_html(title: str, traces: list[dict], layout: dict, note: str) -> str:
    payload = {"traces": traces, "layout": layout}
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><script src="{PLOTLY_CDN}"></script><style>body{{font-family:Georgia,\"Times New Roman\",serif;background:#f5f1e8;color:#1f2a2e;margin:0;padding:2rem}}.wrap{{max-width:1100px;margin:0 auto}}#chart{{width:100%;height:720px}}.note{{color:#4f646b;margin:0 0 1rem 0;line-height:1.5}}</style></head><body><div class="wrap"><h1>{title}</h1><p class="note">{note}</p><div id="chart"></div></div><script>const payload={json.dumps(payload)};Plotly.newPlot("chart",payload.traces,payload.layout,{{responsive:true,displayModeBar:true}});</script></body></html>"""


def color_map_5() -> dict[str, str]:
    return {"1": "#7f1d1d", "2": "#c2410c", "3": "#737373", "4": "#1d4ed8", "5": "#065f46", "Not Rated": "#6b7280"}


def color_map_3() -> dict[str, str]:
    return {"1-2": "#b91c1c", "3": "#737373", "4-5": "#065f46", "Not Rated": "#6b7280"}


def write_visualizations(long_df: pd.DataFrame, panel: pd.DataFrame, viz_dir: Path) -> list[str]:
    created = []
    cmap5 = color_map_5()
    cmap3 = color_map_3()
    years = DISPLAY_YEARS
    chart_years = CHART_YEARS

    def write(name: str, title: str, traces: list[dict], layout: dict, note: str) -> None:
        (viz_dir / name).write_text(plotly_html(title, traces, layout, note), encoding="utf-8")
        created.append(name)

    aggregate5 = (
        long_df[(long_df["rating_bucket_5level"] != "Collapsed") & (long_df["rating_bucket_5level"] != "Not Rated") & (long_df["school_year"].isin(chart_years))]
        .groupby(["school_year", "rating_bucket_5level"], dropna=False, as_index=False)
        .agg({"enrollment": "sum"})
    )
    aggregate3 = (
        long_df[(long_df["rating_bucket_5level"] == "Collapsed") & (long_df["rating_bucket_3level"] != "Not Rated") & (long_df["school_year"].isin(chart_years))]
        .groupby(["school_year", "rating_bucket_3level"], dropna=False, as_index=False)
        .agg({"enrollment": "sum"})
    )

    agg_raw5 = []
    agg_share5 = []
    for bucket in ["1", "2", "3", "4", "5"]:
        ss = aggregate5[aggregate5["rating_bucket_5level"] == bucket].sort_values("school_year")
        agg_raw5.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "name": bucket, "x": ss["school_year"].tolist(), "y": ss["enrollment"].tolist(), "line": {"width": 0.5, "color": cmap5[bucket]}})
        agg_share5.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "groupnorm": "percent", "name": bucket, "x": ss["school_year"].tolist(), "y": ss["enrollment"].tolist(), "line": {"width": 0.5, "color": cmap5[bucket]}})
    write(
        "all_charters_raw_5level.html",
        "All Charter Seats by 1-5 Star Rating",
        agg_raw5,
        {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": chart_years}, "yaxis": {"title": "Seats"}},
        "Stacked trend view of how many charter students were enrolled in 1-star, 2-star, 3-star, 4-star, and 5-star schools over time. Not Rated seats are excluded."
    )
    write(
        "all_charters_share_5level.html",
        "All Charter Seat Share by 1-5 Star Rating",
        agg_share5,
        {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": chart_years}, "yaxis": {"title": "Share (%)", "ticksuffix": "%"}},
        "Same stacked trend, but shown as the share of rated charter seats at each star level instead of raw seat counts. Not Rated seats are excluded."
    )

    agg_raw3 = []
    for bucket in ["1-2", "3", "4-5", "Not Rated"]:
        ss = aggregate3[aggregate3["rating_bucket_3level"] == bucket].sort_values("school_year")
        agg_raw3.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "name": bucket, "x": ss["school_year"].tolist(), "y": ss["enrollment"].tolist(), "line": {"width": 0.5, "color": cmap3[bucket]}})
    write(
        "all_charters_raw_collapsed.html",
        "All Charter Seats by Collapsed Rating Buckets",
        agg_raw3,
        {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": chart_years}, "yaxis": {"title": "Seats"}},
        "Collapsed stacked view using 4-5, 3, and 1-2 buckets. Not Rated seats are excluded."
    )

    for level in LEVEL_ORDER:
        sub5 = long_df[(long_df["level_band"] == level) & (long_df["rating_bucket_5level"] != "Collapsed")]
        raw5 = []
        share5 = []
        for bucket in RATING_ORDER_5:
            ss = sub5[sub5["rating_bucket_5level"] == bucket].sort_values("school_year")
            raw5.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "name": bucket, "x": ss["school_year"].tolist(), "y": ss["enrollment"].tolist(), "line": {"width": 0.5, "color": cmap5[bucket]}})
            share5.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "groupnorm": "percent", "name": bucket, "x": ss["school_year"].tolist(), "y": ss["enrollment"].tolist(), "line": {"width": 0.5, "color": cmap5[bucket]}})
        write(f"{level.lower()}_raw_5level.html", f"{level} Charter Enrollment by 1-5 Star Rating", raw5, {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": years}, "yaxis": {"title": "Enrollment"}}, f"Raw charter enrollment for {level} grades. `2014-15` is shown as a coverage floor but no usable statewide ratings file was recovered for that year.")
        write(f"{level.lower()}_share_5level.html", f"{level} Charter Enrollment Share by 1-5 Star Rating", share5, {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": years}, "yaxis": {"title": "Share (%)", "ticksuffix": "%"}}, f"Share of charter enrollment for {level} grades. `2014-15` is shown as a coverage floor but no usable statewide ratings file was recovered for that year.")

        sub3 = long_df[(long_df["level_band"] == level) & (long_df["rating_bucket_5level"] == "Collapsed")]
        raw3 = []
        share3 = []
        for bucket in RATING_ORDER_3:
            ss = sub3[sub3["rating_bucket_3level"] == bucket].sort_values("school_year")
            raw3.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "name": bucket, "x": ss["school_year"].tolist(), "y": ss["enrollment"].tolist(), "line": {"width": 0.5, "color": cmap3[bucket]}})
            share3.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "groupnorm": "percent", "name": bucket, "x": ss["school_year"].tolist(), "y": ss["enrollment"].tolist(), "line": {"width": 0.5, "color": cmap3[bucket]}})
        write(f"{level.lower()}_raw_collapsed.html", f"{level} Charter Enrollment by Collapsed Rating Buckets", raw3, {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": years}, "yaxis": {"title": "Enrollment"}}, f"Raw charter enrollment for {level} grades, collapsed into 1-2, 3, 4-5, and Not Rated. `2014-15` is included as a visual floor only.")
        write(f"{level.lower()}_share_collapsed.html", f"{level} Charter Enrollment Share by Collapsed Rating Buckets", share3, {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": years}, "yaxis": {"title": "Share (%)", "ticksuffix": "%"}}, f"Share of charter enrollment for {level} grades, collapsed into 1-2, 3, 4-5, and Not Rated. `2014-15` is included as a visual floor only.")

    for filename, title, bucket, metric, note in [
        ("headline_45_seats.html", "4-5 Star Charter Seats Over Time", "4-5", "enrollment", "4-5 star seats by level band."),
        ("headline_45_share.html", "4-5 Star Charter Share Over Time", "4-5", "enrollment_share", "4-5 star charter share by level band."),
        ("headline_12_seats.html", "1-2 Star Charter Seats Over Time", "1-2", "enrollment", "1-2 star seats by level band."),
        ("headline_12_share.html", "1-2 Star Charter Share Over Time", "1-2", "enrollment_share", "1-2 star share by level band."),
    ]:
        traces = []
        sub = long_df[(long_df["rating_bucket_5level"] == "Collapsed") & (long_df["rating_bucket_3level"] == bucket)]
        for level, color in zip(LEVEL_ORDER, ["#8b5cf6", "#0f766e", "#b45309"]):
            ss = sub[sub["level_band"] == level].sort_values("school_year")
            traces.append({"type": "scatter", "mode": "lines+markers", "name": level, "x": ss["school_year"].tolist(), "y": ss[metric].tolist(), "line": {"color": color, "width": 3}, "marker": {"size": 8}})
        layout = {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": years}, "yaxis": {"title": "Share (%)" if metric == "enrollment_share" else "Enrollment"}}
        if metric == "enrollment_share":
            layout["yaxis"]["ticksuffix"] = "%"
        write(filename, title, traces, layout, note)

    totals = panel[panel["school_year"].isin(chart_years)].groupby(["school_year", "school_level_band"], as_index=False)["enrollment_total"].sum()
    traces = []
    for level, color in zip(LEVEL_ORDER, ["#8b5cf6", "#0f766e", "#b45309"]):
        ss = totals[totals["school_level_band"] == level].sort_values("school_year")
        traces.append({"type": "scatter", "mode": "lines+markers", "name": level, "x": ss["school_year"].tolist(), "y": ss["enrollment_total"].tolist(), "line": {"color": color, "width": 3}, "marker": {"size": 8}})
    write("headline_total_enrollment.html", "Total Charter Enrollment Over Time by Level Band", traces, {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": chart_years}, "yaxis": {"title": "Enrollment"}}, "Total charter enrollment by level band across the published quality-seats window. Legacy years are shown directionally, while `2015-16` and `2021-22` are omitted from the chart.")

    level_stack = []
    for level, color in zip(LEVEL_ORDER, ["#8b5cf6", "#0f766e", "#b45309"]):
        ss = totals[totals["school_level_band"] == level].sort_values("school_year")
        level_stack.append({"type": "scatter", "mode": "lines", "stackgroup": "one", "name": level, "x": ss["school_year"].tolist(), "y": ss["enrollment_total"].tolist(), "line": {"width": 0.5, "color": color}})
    write(
        "all_charters_enrollment_by_level.html",
        "All Charter Enrollment by Grade Band",
        level_stack,
        {"paper_bgcolor": "#f5f1e8", "plot_bgcolor": "#fffaf2", "xaxis": {"title": "School Year", "categoryorder": "array", "categoryarray": chart_years}, "yaxis": {"title": "Enrollment"}},
        "Stacked trend view of total charter enrollment split into elementary, middle, and high school seats. Legacy years are shown directionally, while `2015-16` and `2021-22` are omitted from the chart."
    )

    (viz_dir / "visualization_manifest.json").write_text(json.dumps({"generated_files": created, "analysis_years": chart_years, "png_generation": "not attempted because this environment does not currently include a Plotly static image engine such as kaleido"}, indent=2), encoding="utf-8")
    return created


def write_docs(panel: pd.DataFrame, long_df: pd.DataFrame, dirs: dict[str, Path]) -> None:
    four_five = long_df[(long_df["rating_bucket_5level"] == "Collapsed") & (long_df["rating_bucket_3level"] == "4-5")]
    one_two = long_df[(long_df["rating_bucket_5level"] == "Collapsed") & (long_df["rating_bucket_3level"] == "1-2")]
    key = ["# QUALITY_SEATS_KEY_FINDINGS", "", "## Scope", "", "- Historical quality-seats Phase 2 now covers reported charter quality-seats results from `2012-13` through `2024-25`.", "- Public charts now display the legacy years beginning in `2012-13`, with the understanding that `2012-13` through `2014-15` are more directional than the later workbook-based years.", "- `2012-13` through `2014-15` are present as legacy state-charter recoveries using school totals from accountability PDFs plus estimated ES/MS/HS band splits where Nevada did not publish exact band counts.", "- `2015-16` remains in the underlying files as a transition / reset year, but it is omitted from the visible charts because it does not function as a usable rating year in this build.", "- Charter bands are standardized using the statewide suffix convention: `.1 = ES`, `.2 = MS`, `.3 = HS`.", "- Off-band spillover grades in local enrollment workbooks are excluded rather than reassigned across bands.", "- Pandemic / recovery years remain displayed but should be interpreted with caution rather than treated as clean apples-to-apples trend points.", "", "## 4-5 Star Seats", ""]
    for level in LEVEL_ORDER:
        sub = four_five[(four_five["level_band"] == level) & (four_five["enrollment"].notna())].sort_values("school_year")
        key.append(f"- {level}: " + "; ".join(f"{r['school_year']}: {int(r['enrollment']):,}" for _, r in sub.iterrows()))
    key.extend(["", "## 4-5 Star Share", ""])
    for level in LEVEL_ORDER:
        sub = four_five[(four_five["level_band"] == level) & (four_five["enrollment_share"].notna())].sort_values("school_year")
        key.append(f"- {level}: " + "; ".join(f"{r['school_year']}: {r['enrollment_share']:.1%}" for _, r in sub.iterrows()))
    key.extend(["", "## 1-2 Star Seats", ""])
    for level in LEVEL_ORDER:
        sub = one_two[(one_two["level_band"] == level) & (one_two["enrollment"].notna())].sort_values("school_year")
        key.append(f"- {level}: " + "; ".join(f"{r['school_year']}: {int(r['enrollment']):,}" for _, r in sub.iterrows()))
    key.extend(["", "## Pause / comparability notes", ""])
    key.append("- `2019-20`: pandemic disruption at the end of the school year; keep visible but interpret cautiously.")
    key.append("- `2020-21`: pandemic irregular year; keep visible but interpret cautiously.")
    key.append("- `2021-22`: statewide recovery year with many `Not Rated` rows; treat as a pause / reset year, not a standard rating year.")
    (dirs["method"] / "QUALITY_SEATS_KEY_FINDINGS.md").write_text("\n".join(key) + "\n", encoding="utf-8")

    summary = [
        "# EXECUTIVE_SUMMARY_QUALITY_SEATS",
        "",
        "This release measures Nevada charter quality seats as student enrollment by grade band and rating category across a longer historical window.",
        "",
        "- Reported charter quality-seats years in the underlying files: `2012-13` through `2024-25`.",
        "- Public charts now show the legacy years beginning in `2012-13`, excluding `2015-16` and `2021-22` from the visible sequence.",
        "- `2012-13` through `2014-15` are legacy state-charter recoveries, not modern workbook-based joins.",
        "- For multi-band legacy schools, ES/MS/HS seat counts are estimated from the nearest later validation-day band shares because the older PDFs publish school totals but not exact band-level seat counts.",
        "- `2015-16` is retained as a transition year in the data files, but omitted from the visible charts.",
        "- Grade bands are standardized statewide using the published suffix convention rather than LEA-specific grade-span quirks.",
        "- Both raw seats and proportional shares are reported because growth and composition are different policy stories.",
        "- Pandemic / recovery years remain visible but are flagged as less comparable.",
    ]
    (dirs["method"] / "EXECUTIVE_SUMMARY_QUALITY_SEATS.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    readme = [
        "# README_quality_seats_historical",
        "",
        "This package extends the Nevada charter quality-seats analysis backward to the earliest usable statewide rating year currently recovered from direct district downloads.",
        "",
        "## Historical floor",
        "",
        "- Earliest recovered charter quality-seats year in the current build: `2012-13`",
        "- Public charts now display the legacy years beginning in `2012-13`, excluding `2015-16` from the visible sequence.",
        "- `2012-13` through `2014-15` are included as legacy state-charter recoveries with estimated band splits for multi-band schools.",
        "- `2015-16` is retained as a transition year in the data files, but omitted from the visible charts.",
        "- Band rule: `.1 = ES`, `.2 = MS`, `.3 = HS` across all authorizers for consistency and transparency.",
        "- Spillover grades appearing outside a school's published suffix band are excluded rather than reassigned.",
        "",
        "## Pause years",
        "",
        "- `2019-20`: pandemic disruption",
        "- `2020-21`: pandemic irregular",
        "- `2021-22`: recovery / many Not Rated rows",
    ]
    (dirs["method"] / "README_quality_seats_phase2_historical.md").write_text("\n".join(readme) + "\n", encoding="utf-8")


def write_public_overview(dirs: dict[str, Path]) -> None:
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Nevada Charter Quality Seats Historical</title><style>:root{--bg:#f3ecdf;--panel:#fffaf2;--hero:#f7f0e3;--ink:#1f2a2e;--muted:#5b6a70;--accent:#0f5c63;--accent-2:#b45309;--line:#d8cdb8}body{margin:0;font-family:Georgia,\"Times New Roman\",serif;background:linear-gradient(180deg,#eadfc9 0%,var(--bg) 30%,#f9f4ea 100%);color:var(--ink)}main{max-width:1220px;margin:0 auto;padding:1.5rem 1.25rem 4rem}.hero,.slide,.foot{background:var(--panel);border:1px solid var(--line);border-radius:22px;box-shadow:0 12px 32px rgba(31,42,46,.06)}.hero{padding:1.4rem 1.4rem 1.6rem;background:linear-gradient(135deg,var(--hero),var(--panel))}.eyebrow{font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700}.hero h1{font-size:2.4rem;line-height:1.05;margin:.4rem 0 .8rem}.hero p{font-size:1.05rem;line-height:1.55;max-width:980px}.chiprow{display:flex;flex-wrap:wrap;gap:.7rem;margin:1rem 0 0}.chip{background:#fff;border:1px solid var(--line);border-radius:999px;padding:.55rem .9rem;font-size:.92rem}.links{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1rem}.links a{text-decoration:none;color:white;background:var(--accent);padding:.7rem 1rem;border-radius:999px;font-size:.95rem}.links a.alt{background:var(--accent-2)}.deck{display:grid;gap:1.1rem;margin-top:1.1rem}.slide{padding:1.15rem}.slide h2{font-size:1.55rem;line-height:1.15;margin:.15rem 0 .35rem}.slide p{margin:.3rem 0;color:var(--muted);line-height:1.55}.headline{font-size:1.05rem;color:var(--ink);font-weight:700}.iframe-wrap{margin-top:.9rem;border-radius:16px;overflow:hidden;border:1px solid var(--line);background:#fff}.iframe-wrap iframe{width:100%;height:680px;border:0;background:#fff}.foot{margin-top:1.1rem;padding:1rem 1.15rem}.foot h3{margin:.2rem 0 .5rem}.foot ul{margin:.4rem 0 0 1.1rem;color:var(--muted)}@media (min-width:960px){.iframe-wrap iframe{height:620px}}</style></head><body><main><section class=\"hero\"><div class=\"eyebrow\">Nevada Charter Quality Seats</div><h1>How many charter students were in 1-star, 2-star, 3-star, 4-star, and 5-star schools each year?</h1><p>This page now shows the recovered legacy years directly in the charts. The earliest years are more directional than the later workbook-based years, but they are visible because they help tell the actual historical story instead of making the sector look like it suddenly appears in the middle of the timeline.</p><p>The first charts show stacked sectorwide seat counts by star level over time, then sector mix, and only after that total enrollment context. For consistency across authorizers, school bands are standardized statewide as <strong>.1 = ES</strong>, <strong>.2 = MS</strong>, and <strong>.3 = HS</strong>.</p><div class=\"chiprow\"><div class=\"chip\">Visible chart years: <strong>2012-13 to 2024-25</strong></div><div class=\"chip\">Legacy <strong>2012-13 to 2014-15</strong> shown directionally</div><div class=\"chip\"><strong>2015-16</strong> omitted from chart sequence</div><div class=\"chip\"><strong>2021-22</strong> omitted from chart sequence</div></div><div class=\"links\"><a href=\"../03_Clean_Data/quality_seats_summary_wide.csv\">Download Wide Summary</a><a href=\"../03_Clean_Data/quality_seats_school_year_panel.csv\" class=\"alt\">Download School-Year Panel</a><a href=\"../04_Audit_Files/quality_seats_join_audit.csv\">Open Audit File</a><a href=\"../01_Methodology/QUALITY_SEATS_KEY_FINDINGS.md\">Open Key Findings</a></div></section><section class=\"deck\"><section class=\"slide\"><div class=\"eyebrow\">Slide 1</div><h2>All charter seats by 1-5 star rating</h2><p class=\"headline\">This is the main question: how many students were in low-, middle-, and high-performing charter schools each year?</p><p>Read it like a stacked bar chart stretched over time. The bottom layer is one star, then two star, then three, then four, then five. The legacy years are shown for directionality, while <strong>2015-16</strong> and <strong>2021-22</strong> remain omitted because they do not function like standard rating years in this build.</p><div class=\"iframe-wrap\"><iframe src=\"../05_Visualizations/all_charters_raw_5level.html\"></iframe></div></section><section class=\"slide\"><div class=\"eyebrow\">Slide 2</div><h2>All charter seat share by 1-5 star rating</h2><p class=\"headline\">This shows whether the sector mix is changing, not just whether the sector is getting bigger.</p><p>If the upper bands take up more of the chart over time, a larger share of rated charter seats is being served in higher-rated schools. If the lower bands expand, more students are being served in lower-performing schools.</p><div class=\"iframe-wrap\"><iframe src=\"../05_Visualizations/all_charters_share_5level.html\"></iframe></div></section><section class=\"slide\"><div class=\"eyebrow\">Slide 3</div><h2>Collapsed view: 1-2, 3, and 4-5</h2><p class=\"headline\">This is the simpler policy version when a five-layer chart feels too busy.</p><p>It preserves the same bottom-to-top logic: lower-performing schools sit at the bottom, middle-performing schools in the middle, and higher-performing schools on top. Seats with no quality indicator are still excluded.</p><div class=\"iframe-wrap\"><iframe src=\"../05_Visualizations/all_charters_raw_collapsed.html\"></iframe></div></section><section class=\"slide\"><div class=\"eyebrow\">Slide 4</div><h2>Total charter enrollment context by grade band</h2><p class=\"headline\">This is the supporting enrollment view: how the charter sector itself changed across elementary, middle, and high school seats.</p><p>Use it to understand the scale behind the rating charts above. The legacy years are shown directionally here as well, while <strong>2015-16</strong> and <strong>2021-22</strong> remain omitted.</p><div class=\"iframe-wrap\"><iframe src=\"../05_Visualizations/all_charters_enrollment_by_level.html\"></iframe></div></section></section><section class=\"foot\"><h3>Important reading notes</h3><ul><li><strong>2012-13</strong> through <strong>2014-15</strong> come from legacy state-charter accountability recoveries rather than the later modern workbook pipeline.</li><li>For multi-band legacy schools, ES/MS/HS seat counts are estimated from the nearest later validation-day band shares because the older PDFs publish school totals but not exact band-level seat counts.</li><li><strong>2015-16</strong> is still best understood as a transition year, but it is retained in the download files rather than shown in the visible chart sequence.</li><li><strong>2021-22</strong> is omitted from the public chart sequence rather than being shown as a pseudo-comparable rating year.</li><li>Seats in <strong>Not Rated</strong> schools are excluded from the main rating charts because they do not carry a usable quality indicator.</li><li>Grade bands are standardized statewide using the published suffix convention rather than LEA-specific grade-span quirks.</li><li>When local enrollment workbooks show spillover grades outside the published suffix band, those seats are excluded rather than reassigned.</li><li>A very small number of rows remain in a manual-review bucket for later research; they are not forced into the published totals.</li></ul></section></main></body></html>"""
    (dirs["web"] / "quality-seats-overview.html").write_text(html, encoding="utf-8")
    (dirs["web"] / "index.html").write_text("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta http-equiv='refresh' content='0; url=quality-seats-overview.html'><title>Nevada Charter Quality Seats Historical</title></head><body><p><a href='quality-seats-overview.html'>Open the quality seats overview page</a></p></body></html>", encoding="utf-8")


def copy_sources(dirs: dict[str, Path]) -> None:
    extras = [SOURCE_DIR / "nspf" / "README.md"]
    for legacy_src in [LEGACY_PANEL_FILE, LEGACY_TOTALS_FILE, LEGACY_AUDIT_FILE]:
        if legacy_src.exists():
            extras.append(legacy_src)
    for src in set([info["ratings"] for info in ANALYSIS_YEARS.values()] + list(ARCHIVED_ENROLLMENT_FILES.values()) + extras):
        if Path(src).exists():
            shutil.copy2(src, dirs["source"] / Path(src).name)


def write_manifest(dirs: dict[str, Path], charts: list[str]) -> None:
    (dirs["log"] / "release_manifest.json").write_text(json.dumps({"release_name": "NV_Charter_Quality_Seats_v2", "analysis_years": DISPLAY_YEARS, "public_page": "06_Public_Website/quality-seats-overview.html", "chart_count": len(charts)}, indent=2), encoding="utf-8")
    (dirs["log"] / "CHANGELOG.md").write_text("# CHANGELOG\n\n- Extended charter quality seats series backward to 2015-16 using direct district NSPF downloads.\n- Added 2014-15 as an explicit presentation-floor year with no recovered statewide ratings values.\n- Fixed the 2015-16 legacy enrollment parser so grade codes like 01/06 join correctly to elementary and middle school bands.\n- Added historical seat and share charts with pause-year caveats.\n- Confirmed 2013-14 district rating pulls are header-only placeholders, not usable statewide data files.\n", encoding="utf-8")


def main() -> None:
    dirs = ensure_dirs()
    copy_sources(dirs)
    panel, audit, source_manifest = build_quality_panel()
    panel = panel.sort_values(["school_year", "district_code", "school_code"]).reset_index(drop=True)
    audit = audit.sort_values(["school_year", "issue_type", "school_code"]).reset_index(drop=True)
    source_manifest = source_manifest.drop_duplicates(subset=["file_name", "source_url"]).reset_index(drop=True)
    summary_long, summary_wide = build_summaries(panel)
    panel.to_csv(dirs["clean"] / "quality_seats_school_year_panel.csv", index=False)
    summary_long.to_csv(dirs["clean"] / "quality_seats_summary_long.csv", index=False)
    summary_wide.to_csv(dirs["clean"] / "quality_seats_summary_wide.csv", index=False)
    panel.to_csv(dirs["clean"] / "quality_seats_panel.csv", index=False)
    summary_wide.to_csv(dirs["clean"] / "quality_seats_summary.csv", index=False)
    summary_long.to_csv(dirs["clean"] / "quality_seats_by_grade_band.csv", index=False)
    summary_long[["school_year", "level_band", "rating_bucket_5level", "rating_bucket_3level", "enrollment_share"]].to_csv(dirs["clean"] / "quality_seats_share.csv", index=False)
    audit.to_csv(dirs["audit"] / "quality_seats_join_audit.csv", index=False)
    source_manifest.to_csv(dirs["audit"] / "source_manifest_quality_seats.csv", index=False)
    charts = write_visualizations(summary_long, panel, dirs["viz"])
    write_docs(panel, summary_long, dirs)
    write_public_overview(dirs)
    write_manifest(dirs, charts)
    zip_path = ROOT / "release" / "NV_Charter_Quality_Seats_v2.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(RELEASE_ROOT.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(RELEASE_ROOT.parent))


if __name__ == "__main__":
    main()
