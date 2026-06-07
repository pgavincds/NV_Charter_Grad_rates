# README_quality_seats_historical

This package extends the Nevada charter quality-seats analysis backward to the earliest usable statewide rating year currently recovered from direct district downloads.

## Historical floor

- Earliest recovered charter quality-seats year in the current build: `2012-13`
- Public charts now display the legacy years beginning in `2012-13`, excluding `2015-16` from the visible sequence.
- `2012-13` through `2014-15` are included as legacy state-charter recoveries with estimated band splits for multi-band schools.
- `2015-16` is retained as a transition year in the data files, but omitted from the visible charts.
- Band rule: `.1 = ES`, `.2 = MS`, `.3 = HS` across all authorizers for consistency and transparency.
- Spillover grades appearing outside a school's published suffix band are excluded rather than reassigned.

## Pause years

- `2019-20`: pandemic disruption
- `2020-21`: pandemic irregular
- `2021-22`: recovery / many Not Rated rows
