# Weighted Phase 1 Method Note

This Phase 1 rebuild uses weighted ACGR as the primary sector measure:

`weighted_acgr = sum(graduates) / sum(cohort)`

The purpose is to describe what happened to the average student in Nevada's charter high-school sector rather than the average school.

## Core rules

1. Legal charter status is separate from school-choice status. District-operated choice, virtual, alternative, and contract schools are excluded even when they appear in the same public reporting universe.
2. Validation Day enrollment files are used to verify grade-12 presence, not as ACGR denominators.
3. Published Nevada ACGR values are preserved as the official point values when they conflict with numerator/denominator-derived rates; those conflicts are flagged in `data_validation_exceptions.csv`.
4. Closed-school cases such as ICDA are documented separately so post-closure student outcomes are not attributed back to the charter without clear public support.
5. Early years were compositionally different: large online and alternative operators dominated the charter high-school denominator before many later brick-and-mortar operators expanded into grade 12.
