# Nevada Charter Graduation Rates

This repository assembles a public, reproducible estimate of Nevada charter-sector 4-year graduation rates alongside official statewide and district comparison rates.

It is designed to work in two formats at the same time:

- as a GitHub repository that others can inspect, reuse, or contribute to
- as a public web artifact that can live on an existing site under a descriptive direct-link URL

## Start Here

- Narrative landing page: `nevada-charter-graduation-rates-overview.html`
- Data page: `nevada-charter-graduation-rates.html`
- Wide trend table: `nevada_charter_publishable_trend_table.csv`
- Chart-ready long table: `nevada_charter_publishable_series_long.csv`
- Short explainer: `README_nevada_charter_grad_rates.md`
- Full method memo: `nevada_charter_grad_rate_method.md`

## What The Repository Publishes

The public package distinguishes between:

- official public rates reported by the Nevada Department of Education
- estimated charter-sector slices built from school-level public rows

Official comparison rows include:

- statewide Nevada
- State Public Charter School Authority
- adjusted SPCSA charter-only estimate shown separately from the official public sponsor rate
- Achievement School District where separately reported
- Clark County School District
- Washoe County School District
- Carson City School District

Estimated charter slices include:

- SPCSA adjusted charter-only
- SPCSA brick and mortar
- SPCSA general education virtual
- Nevada Connections reported separately
- Nevada Virtual reported separately
- Leadership Academy reported separately
- Beacon reported separately
- Clark charter total
- Clark brick and mortar
- Clark alternative
- Washoe charter total
- Washoe brick and mortar
- Washoe alternative watchlist

## Public Files

- `nevada_charter_publishable_trend_table.csv`
  Year-by-year wide table for direct reading and download sharing.
- `nevada_charter_publishable_series_long.csv`
  Long-format chart table for spreadsheet work, GitHub previews, and web charts.
- `nevada-charter-graduation-rates-overview.html`
  Shorter public narrative page.
- `nevada-charter-graduation-rates.html`
  More data-forward page with direct file links and a summary table.

## Working Files

- `nevada_charter_school_year_panel.csv`
  Main school-year source panel.
- `nevada_charter_panel_decisions.csv`
  Decision ledger showing whether each school-year is counted, held, or excluded.
- `nevada_charter_panel_decision_summary.csv`
  By-year coverage snapshot.
- `nevada_grade12_crosscheck_tracker.csv`
  Grade-12 enrollment cross-check tracker for unresolved or excluded rows.
- `nevada_charter_legacy_universe_2015_16_to_2019_20.csv`
  Legacy-year crosswalk and control file.

## Ground Rules

- Historical authorizer is tied to the reporting year.
- District-operated option schools are excluded if they were not created under Nevada charter law.
- Non-charter statewide entities such as `Davidson` / `University Schools` and `Independence` / the correctional LEA are excluded from every charter slice even if historical official sponsor totals may still warrant a caveat.
- Beacon is reported separately because of its alternative / APF treatment.
- Early SPCSA school-level slices for `2013-14` through `2016-17` are partially backfilled from direct Nevada Report Card portal queries.
- Early Clark and Washoe charter totals are now partially backfilled through `2016-17` from Nevada Report Card exports and portal recovery.
- Small or suppressed public rows are handled with interval treatment rather than fake precision.
- When grade-by-grade enrollment shows no 12th grade, the school-year is excluded from the 4-year graduation universe unless a contrary public ACGR row exists.
- Leadership Academy is now reported separately alongside the virtual schools, but it remains coded as `alternative` in the working panel rather than `statewide_online`.
- The adjusted SPCSA charter-only line is especially useful in the older years, when public sponsor totals were more vulnerable to legacy aggregation issues; the gap should generally be read more cautiously in the cleaner post-2018 files.

## Contributing

If someone wants to help improve the project, the cleanest place to start is the school-year decision ledger and the methodology memo. See `CONTRIBUTING.md` for the preferred workflow and file priorities.

## Suggested Public URL Pattern

If this is hosted on your existing site, descriptive filenames like these work better than `index.html`:

- `nevada-charter-graduation-rates-overview.html`
- `nevada-charter-graduation-rates.html`

That keeps the pages shareable without making them look like the homepage of the broader site.
