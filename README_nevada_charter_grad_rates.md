# Nevada Charter Graduation Rates

This folder contains a public-facing build of estimated Nevada charter-sector 4-year graduation rates alongside official statewide and district comparison rates.

## Main files

- `nevada_charter_publishable_trend_table.csv`: wide year-by-year trend table for direct reading.
- `nevada_charter_publishable_series_long.csv`: chart-friendly long table for GitHub, spreadsheets, and simple visualizations.
- `nevada_charter_sector_trend_table.csv`: working output table used to generate the publishable files.
- `nevada_charter_school_year_panel.csv`: school-year source panel.
- `nevada_charter_panel_decisions.csv`: school-year decision ledger showing whether each row is counted, held, or excluded.
- `nevada_charter_grad_rate_method.md`: full methodology memo.

## What is official

Official public rates come from Nevada Department of Education annual 4-year ACGR releases and are shown for:

- statewide Nevada
- SPCSA as a public authorizer total
- Achievement School District where separately reported
- Clark County School District
- Washoe County School District
- Carson City School District

## What is estimated

The charter slices are estimated from school-level public rows and are not official sponsor-published subgroup rates unless explicitly noted otherwise. These include:

- `spcsa_adjusted_charter_only`
- `spcsa_brick_mortar`
- `spcsa_general_ed_virtual`
- `spcsa_nevada_connections`
- `spcsa_nevada_virtual`
- `spcsa_leadership_academy`
- `beacon_separate`
- `clark_charter_total`
- `clark_brick_mortar`
- `clark_alternative`
- `washoe_charter_total`
- `washoe_brick_mortar`
- `washoe_alternative_watchlist`

## Suppression rule

When Nevada suppresses or top-codes school-level values, the working estimates use interval treatment:

- `+` is treated as `95.0` to `100.0`, midpoint `97.5`
- `*` is treated as `0.0` to `5.0`, midpoint `2.5`

## Key interpretation cautions

- Historical authorizer is tied to the reporting year. A later sponsor transfer does not change earlier rows.
- `Democracy Prep` is treated as an `Achievement School District` school for `2017-18` and `2018-19`, then as an SPCSA school afterward.
- `Beacon` is broken out separately because of its alternative / APF treatment.
- `Nevada Connections`, `Nevada Virtual`, and `Leadership Academy` are now shown as separate SPCSA reported lines rather than only inside the aggregate SPCSA virtual bucket; `Leadership Academy` remains coded as `alternative` in the working panel.
- District-operated option schools such as `NV Learning Academy` and `North Star Online School` are excluded because they were not charter schools under Nevada charter law.
- Many early apparent “missing” rows turned out to be schools that had not yet reached 12th grade. Those are now excluded rather than held.
- The one remaining modern hold is `2018-19 NSHS Meadowwood`, which is still public as a very small suppressed cohort rather than a recoverable exact rate.

## Historical recovery source

For older school-by-school rows, the Nevada Report Card student interface turned out to be the strongest public source:

- `https://nevadareportcard.nv.gov/di/main/students`

Nevada's own FAQ says the portal provides school-level accountability data going back to 2003, including graduation rates. Using that portal, the project now backfills a meaningful SPCSA school-level layer for `2013-14` through `2016-17`, including legacy rows for `Alpine`, `Beacon`, `Nevada Connections`, `Nevada Virtual`, `Quest`, the pre-campus-split `Nevada State High School` row, and the `Silver State` / `Argent` lineage. The same portal workflow, together with downloaded multi-year exports, now also backfills early Clark and Washoe charter totals through `2016-17`, including legacy rows for `Innovations`, `Odyssey`, `Explore Knowledge`, `Delta`, `ACE`, `Coral`, `ICDA`, and `enCompass` / `Rainshadow`.

The downloaded multi-year export also shows Davidson only as its own school row, not as a visible `University Schools` aggregate row. That does not prove historical sponsor totals were never contaminated, but it does mean this school-level export is best used to recover individual school rows rather than to settle old aggregate-reporting disputes by itself.

The same approach applies to `Independence` and the correctional LEA context. In this project, `Davidson` and `Independence` are treated as non-charter rows and excluded from the weighted-average construction of every SPCSA charter slice, including `SPCSA brick and mortar`, `SPCSA virtual`, `SPCSA alternative`, and the separate school-level SPCSA breakout lines. If a historical official sponsor total may have absorbed one of those schools, that possibility is carried as a caveat on the official comparator rather than silently folded into the charter estimate.

That is why the public outputs now distinguish between:

- `SPCSA official public`: Nevada's published sponsor total
- `SPCSA adjusted charter-only`: the screened charter-only estimate built from counted SPCSA charter rows after excluding non-charter entities such as `Davidson` and `Independence`

The adjusted line is most informative in the older years, when sponsor-level public aggregation appears more vulnerable to mixed-entity reporting. The post-2018 files appear substantially cleaner, so later official-versus-adjusted differences should be read more cautiously.

## Replication Steps

Researchers who want to duplicate or challenge this build can follow the same sequence:

1. Download the official annual Nevada 4-year ACGR PDFs for the years in scope and use them as the controlling source for statewide, district, and sponsor totals.
2. Download Nevada Report Card school-level exports or direct portal views for the same years, especially for legacy recovery before the cleaner modern PDF series.
3. Build a school-year universe keyed first to entity ID, then to school name, authorizer, and school model so renamed schools can be tracked consistently across years.
4. Exclude schools that were not charter schools under Nevada charter law in the reporting year, including district option schools and non-charter statewide entities such as `Davidson` and `Independence`.
5. Cross-check unresolved rows against Nevada's grade-by-grade enrollment files to confirm whether a school actually had 12th graders in that year.
6. Apply Nevada's public suppression rules consistently: `+` becomes `95.0 / 97.5 / 100.0`, `*` becomes `0.0 / 2.5 / 5.0`, and `NA` remains outside exact aggregation unless another defensible public value can be recovered.
7. Keep official public sponsor totals separate from charter-slice estimates. If school-level evidence suggests an official historical sponsor total may have included non-charter entities, note that as a caveat rather than rewriting the official comparator.
8. Regenerate the year-by-year trend tables from the school-year panel and decision ledger so every counted, held, or excluded row can be audited.

## Suggested citation language

"Estimated Nevada charter-sector graduation rate series assembled from Nevada Department of Education annual 4-year ACGR files, related public accountability materials, and school-year enrollment cross-checks. Official statewide and district authorizer totals are reproduced as published; charter subgroup slices are estimated from school-level public records."
