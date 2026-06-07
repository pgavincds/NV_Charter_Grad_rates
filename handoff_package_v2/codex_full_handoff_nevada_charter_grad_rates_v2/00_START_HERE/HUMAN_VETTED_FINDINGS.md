# Human-Vetted Findings Codex Should Treat as Starting Assumptions

These are findings reached through review of the uploaded ACGR exports, Validation Day enrollment files, Nevada charter-board materials, public closure reporting, and manual reasoning. Codex should not waste tokens rediscovering these from scratch. It should validate them while implementing the pipeline.

## Calculation finding

Sector-level rates must be recalculated as weighted ACGR:

```text
weighted_acgr = sum(graduates) / sum(cohort)
```

This changes the question from "what was the average school rate?" to "what happened to the average student in the sector?"

## Reporting-year convention

Nevada reports cohort graduation outcomes in the subsequent accountability/reporting year.

Example:

| Operating school year | Accountability / reporting year |
|---|---|
| 2023-24 | 2024-25 |
| 2022-23 | 2023-24 |

Therefore every row should preserve separate fields for:

```text
operating_school_year
accountability_reporting_year
graduating_class_year
```

## Legal charter status rule

A school is included only if it was legally operating as a Nevada charter school during the relevant year. District-operated choice, virtual, magnet, alternative, or contract schools are excluded even if families could choose them or the district contracted with K12, Ombudsman, or another vendor.

Known exclusions:

- Northeastern Nevada Virtual Academy
- NV Learning Academy
- North Star Online
- White Pine district-operated virtual programs
- District-operated alternative/contract schools

## Graduation-universe rule

A school enters the graduation-rate universe when it has grade 12 enrollment and/or an ACGR row. Validation Day enrollment files are used to validate grade-12 presence. They are not ACGR denominators.

## Known school decisions

### YWLA

Exclude through 2024-25. Board materials and enrollment evidence show no graduating cohort as of the years reviewed. Treat as `not_yet_in_graduation_universe`.

### Explore Academy

Validation Day review indicates no grade 12 in 2021-22 or 2022-23; grade 12 first appears in 2023-24 operating year. First possible 4-year ACGR reporting year is 2024-25. Exclude prior years.

### Quest Academy

Do not auto-exclude. The current reconstructed panel shows reported ACGR rows for 2013-14 through 2016-17. Codex should determine the last year with grade 12 using Validation Day/enrollment and ACGR evidence.

### ICDA / I Can Do Anything Charter High School

Include reported cohorts through the final reported cohort in the portal exports. Do not impute post-closure cohorts or treat displaced students as zero-graduation outcomes. Document as a closure/transition case.

### Northeastern Nevada Virtual Academy

Exists as its own NDE reporting row, but the 04 organization-code prefix and operational understanding point to district operation, not SPCSA charter status. Exclude from charter universe.

## Published value conflicts

If Nevada's published ACGR conflicts with the ACGR derived from the same row's displayed numerator/denominator, use Nevada's published ACGR as the official school-level point value, but flag the conflict.

Create `data_validation_exceptions.csv` for discrepancies greater than 0.5 percentage points.

Example discussed: Quest 2013-14 appeared to show a mismatch between published rate and numerator/denominator-derived value. Preserve the published value and flag.

## Interpretation finding

The early Nevada charter high-school universe was not representative of the later charter sector. Early student-weighted rates were strongly shaped by large statewide online schools and alternative programs. Many later high-performing brick-and-mortar operators were K-8 or otherwise had not yet expanded into grade 12.

The public data story should therefore include both:

1. rate trends, and
2. growth in graduating students / sector composition.
