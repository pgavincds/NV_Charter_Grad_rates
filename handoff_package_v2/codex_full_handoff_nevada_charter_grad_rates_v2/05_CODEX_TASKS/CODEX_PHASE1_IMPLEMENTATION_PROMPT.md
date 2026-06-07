# Codex Task — Phase 1 Implementation

## Goal

Using the files in this package, implement the first reproducible rebuild of the Nevada Charter Graduation Rates project using weighted ACGR, documented universe decisions, source manifests, and persuasive visualizations.

Do not do a sprawling full redesign yet. Produce clean data, audit outputs, and a public visualization starter.

## Inputs

Use the source files in:

```text
01_SOURCE_DATA/
02_CURRENT_REPO_INPUTS/
03_PRIOR_CALCULATED_OUTPUTS/
04_DECISION_REGISTERS/
```

## Primary calculation

For all sector-level aggregations:

```text
weighted_acgr = sum(total_graduates) / sum(total_cohort)
```

Do not use average-of-school rates as the headline measure.

Retain unweighted campus averages only as supplemental context.

## Required outputs

Create a new output directory:

```text
release/NV_Charter_Grad_Rates_Weighted_Rebuild_v1/
```

with these subdirectories:

```text
01_Methodology/
02_Source_Data/
03_Clean_Data/
04_Audit_Files/
05_Visualizations/
06_Public_Website/
07_Change_Log/
```

## Required clean data files

### weighted_sector_series.csv

Rows for:

- statewide official
- SPCSA official
- Clark official
- Washoe official
- SPCSA charter-only weighted
- SPCSA brick-and-mortar weighted
- SPCSA virtual weighted
- SPCSA alternative weighted
- Clark charter total weighted
- Washoe charter total weighted

Fields:

```text
year
series_id
series_label
cohort
graduates
weighted_acgr
low_acgr
likely_acgr
high_acgr
included_school_count
suppressed_school_count
notes
```

### graduation_universe.csv

Fields:

```text
school_name
school_code
authorizer
model_type
operating_school_year
accountability_reporting_year
legal_charter
grade_9_count
grade_10_count
grade_11_count
grade_12_count
has_grade_12
acgr_row_exists
include_in_charter_grad_universe
exclusion_reason
confidence
source_file
source_url
date_accessed
```

### school_lifecycle_report.csv

Fields:

```text
school_name
school_code
authorizer
model_type
first_grade12_year
last_grade12_year
first_acgr_year
last_acgr_year
closure_year
transition_notes
```

### data_validation_exceptions.csv

For every school-year with cohort, graduates, and published ACGR, derive graduates/cohort and compare to published ACGR. Flag discrepancies greater than 0.5 percentage points.

Fields:

```text
school_name
school_code
year
published_acgr
derived_acgr
difference
cohort
graduates
notes
```

### uncertainty_register.csv

Fields:

```text
school_name
school_code
year
uncertainty_type
low_value
likely_value
high_value
impact_level
notes
source
```

Uncertainty types:

- suppression
- internal_state_data_conflict
- closure_attribution
- legal_status
- no_grade_12
- entity_code_transition
- authorizer_transition

### source_manifest.csv

Fields:

```text
source_type
file_name
source_url
date_accessed
sha256
notes
```

## Required visualizations

Create `scripts/build_visualizations.py` using pandas + plotly. Generate standalone HTML charts and static PNGs where feasible under `05_Visualizations/`.

Required charts:

1. Weighted ACGR trend
   - Statewide official
   - SPCSA official
   - SPCSA charter-only weighted
   - SPCSA brick-and-mortar weighted
   - SPCSA virtual weighted
   - SPCSA alternative weighted

2. Graduates produced by year
   - Total charter graduates by year
   - Prefer stacked by model if the classification is ready

3. Cohort size by model over time
   - brick-and-mortar
   - virtual
   - alternative

4. Weighted vs unweighted comparison
   - previous unweighted campus average
   - new weighted ACGR
   - Note: "Unweighted = average school. Weighted = average student."

5. Top contributors by year
   - Top schools by graduates and/or cohort share for at least 2013-14, 2018-19, 2024-25

## Required narrative outputs

### README_weighted_phase1.md

Explain:

1. Why weighted ACGR replaces unweighted averages.
2. Why legal charter status is separate from school-choice/virtual status.
3. Why Validation Day files verify grade 12 presence but are not denominators.
4. Why closed-school cases like ICDA are documented separately.
5. Why uncertainty is data-quality uncertainty, not a traditional statistical confidence interval.
6. Why early years were dominated by large online/alternative operators while later high-performing brick-and-mortar high school seats emerged.

### KEY_FINDINGS.md

Answer:

1. How many charter graduates were produced each year?
2. How much did the high-school sector grow?
3. Which operators contributed the most graduates?
4. How much of early SPCSA performance was driven by virtuals?
5. How different are weighted and unweighted results?
6. Which assumptions matter most?

### CHANGELOG.md

Sections:

- Major methodological changes
- Data corrections
- Inclusion/exclusion changes
- Closure cases
- Remaining open questions
- Future research

## Do not do yet

- Do not delete prior unweighted outputs.
- Do not silently resolve data conflicts.
- Do not treat unmatched rows as errors automatically.
- Do not overbuild the full website before the data/audit outputs are reviewed.

Stop after producing the Phase 1 release package and summarize findings.
