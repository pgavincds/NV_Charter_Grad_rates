# Nevada Charter Graduation Rates — Codex Full Handoff v2

This package is meant to let Codex **implement**, not rediscover, the methodology and evidence already vetted in the ChatGPT analysis session.

## What this package contains

1. Actual Nevada Report Card ACGR CSV exports that include cohort counts, graduate counts, and graduation rates.
2. Actual Nevada Validation Day enrollment workbooks for 2021-22 through 2025-26.
3. The current reconstructed charter school-year panel from the existing repo.
4. Prior weighted recalculation outputs already produced in the analysis session.
5. Human-vetted decision registers for known edge cases.
6. A Codex Phase 1 task prompt focused on weighted reconstruction, source documentation, and compelling public visualizations.

## Core correction

The existing public project used many sector aggregates that were effectively unweighted averages of school-level rates. The corrected primary metric is weighted ACGR:

```text
weighted_acgr = sum(total_graduates) / sum(total_cohort)
```

Unweighted school averages may be retained as a supplemental statistic, but must not be the headline sector graduation rate.

## Do not skip

Codex must produce source manifests, uncertainty registers, validation exceptions, and lifecycle/universe tables alongside visualizations. The purpose is not just to make charts; it is to make a reproducible public artifact.
