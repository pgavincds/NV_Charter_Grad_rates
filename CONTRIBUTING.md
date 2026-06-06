# Contributing

This project mixes public data recovery, legacy school crosswalk work, and methodological judgment. The easiest way to contribute well is to improve the evidence trail first and the output files second.

## Best Places To Contribute

- `nevada_charter_school_year_panel.csv`
  Add or correct school-year ACGR rows.
- `nevada_charter_panel_decisions.csv`
  Clarify whether a school-year should be counted, held, or excluded.
- `nevada_grade12_crosscheck_tracker.csv`
  Resolve unresolved rows using grade-by-grade enrollment files.
- `nevada_charter_grad_rate_method.md`
  Improve transparency when a rule changes.

## Preferred Workflow

1. Verify the school-year universe first.
2. Confirm whether the school had 12th grade in that year.
3. Recover the public ACGR row if one exists.
4. Update the decision ledger so the count / hold / exclude rule is explicit.
5. Refresh any affected summary or trend files.

## Ground Rules

- Keep historical authorizer tied to the reporting year.
- Do not treat district option schools as charters.
- Do not back-cast later sponsor transfers into earlier years.
- If a public ACGR row exists, use it.
- If no public ACGR row exists and enrollment shows no 12th grade, exclude the school-year from the 4-year graduation universe.
- If a row is still ambiguous, prefer an explicit hold note over a silent assumption.

## Documentation Norm

If a rule changes, update both:

- the relevant CSV row or rows
- `nevada_charter_grad_rate_method.md`

That keeps the public artifact and the methodology memo aligned.
