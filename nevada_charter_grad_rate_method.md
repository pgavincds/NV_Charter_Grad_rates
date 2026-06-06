# Nevada Charter Sector Graduation Rate Method

## Scope

This note lays out a practical way to estimate Nevada's charter-sector 4-year Adjusted Cohort Graduation Rate (ACGR) from Nevada's first ACGR reporting year through the present.

Nevada's FAQ says the first four-year ACGR report was released in fall 2011 for the graduating class of 2011, covering students who entered high school in 2007-08.

For immediate build purposes, the structured files in this workspace are strongest from the Class of 2018-19 forward and are being extended backward year by year.

The workspace now also includes a legacy control file, `nevada_charter_legacy_universe_2015_16_to_2019_20.csv`, that is meant to function as the year-specific inclusion and holdout ledger for the riskiest historical period.

It also now includes `nevada_charter_panel_decisions.csv`, a whole-panel decision ledger that assigns each school-year to a universe decision, a rate decision, and a count / hold / no action for estimation purposes.

It also now includes enrollment cross-check support files so unresolved school-years can be tested against Nevada's annual enrollment-by-grade spreadsheets before we decide whether a school truly belonged in the 12th-grade graduation universe for that year.

The goal is to produce:

1. A statewide charter-sector rate that includes both SPCSA-authorized and district-authorized charters.
2. Separate breakout rates for:
   - traditional brick-and-mortar charters
   - statewide online charters
   - alternative / credit-recovery charters
3. A transparent treatment of suppression and top/bottom coding.
4. A comparison framework that explicitly separates SPCSA, ASD where historically applicable, Clark-sponsored charters, Washoe-sponsored charters, statewide, and district official public rates.

For the legacy classes before 2017-18, the most realistic build sequence is:

1. recover statewide and district official rates first
2. recover SPCSA sponsor and school-level rates from annual report cards and board materials
3. then extend the full school-year panel backward once the older school-name and entity crosswalk is stable

That sequence is now partially underway through a separate official-comparison spine file that captures statewide, SPCSA, Clark, Washoe, and Carson public rates by class year before every school-level charter slice is fully rebuilt.

## Target comparison structure

The intended reporting structure is:

1. Statewide official public rate
2. A companion table with each Nevada district or sponsor's official public rate from the annual NDE file
3. Official public rates for SPCSA, ASD where separately reported, Clark, Washoe, and Carson preserved as distinct comparison rows
4. SPCSA total
5. SPCSA brick-and-mortar
6. SPCSA general education virtual
7. SPCSA alternative / APF breakout
8. Beacon Academy separate breakout
9. Clark-sponsored charter total
10. Clark-sponsored charter brick-and-mortar
11. Clark-sponsored charter general education virtual
12. Clark-sponsored charter alternative / APF breakout
13. Washoe-sponsored charter total
14. Washoe-sponsored charter brick-and-mortar
15. Washoe-sponsored charter general education virtual
16. Washoe-sponsored charter alternative / APF breakout if formally justified

Important note:

- Carson City is not part of the high-school charter comparison structure because the Carson-authorized charter referenced in current NDE materials is an elementary Montessori school rather than a charter high school.

## Charter Universe Rule

Before a school is included in any charter graduation-rate slice, verify that it was actually operating as a charter school under Nevada charter law in the reporting year.

For this project, the key practical distinction is:

- include schools operating under Nevada charter statute and a valid charter sponsor or authorizer for that year
- exclude district option schools, virtual district schools, magnets, and other district-operated specialty schools even if they are sometimes described informally as charter-like

Two corrected examples from this workspace are useful reminders:

- `NV Learning Academy` is a Clark district school and does not belong in the charter universe
- `North Star Online School` is a Washoe district school and does not belong in the charter universe

That rule should be treated as more important than marketing language, school-choice branding, or parent perception.

## Core Source Set

### 1. Nevada Accountability Portal annual 4-year ACGR PDFs

These are the cleanest public source for school-level charter rates.

- Class of 2024-25: https://nevadareportcard.nv.gov/DI/MoreDownload?filename=Class+of+2024-2025+4+Year+ACGR.pdf
- Class of 2023-24: https://nevadareportcard.nv.gov/DI/MoreDownload?filename=4+Year+Graduation+Rates+for+the+Class+of+2023-24.pdf
- Class of 2022-23: https://nevadareportcard.nv.gov/DI/MoreDownload?filename=4+Year+Graduation+Rates+for+the+Class+of+2022-23.pdf
- Class of 2021-22: https://nevadareportcard.nv.gov/DI/MoreDownload?filename=4+Year+Graduation+Rates+for+the+Class+of+2021-22.pdf
- Class of 2020-21: https://nevadareportcard.nv.gov/DI/MoreDownload?filename=4+Year+Graduation+Rates+for+the+Class+of+2020-21.pdf
- Class of 2019-20: https://nevadareportcard.nv.gov/DI/MoreDownload?filename=4+Year+Graduation+Rates+for+the+Class+of+2019-20.pdf
- Class of 2018-19: https://nevadareportcard.nv.gov/DI/MoreDownload?filename=4+Year+Graduation+Rates+for+the+Class+of+2018-2019.pdf
- Class of 2017-18: https://webapp-strapi-paas-prod-nde-001.azurewebsites.net/uploads/suppressed1718_afee2482a5.pdf

The resource page where Nevada posts these files is:

- https://nevadareportcard.nv.gov/di//Resources

For earlier years, the portal FAQ and legacy report-card materials indicate ACGR reporting goes back to the graduating class of 2011.

In practice, that means the project should distinguish between two phases of evidence:

- `2018-19 forward`: relatively standardized statewide annual ACGR PDFs are posted on the current Nevada resources page
- `2011 through 2017-18`: legacy recovery will rely more heavily on FAQ-confirmed portal history, annual report cards, board attachments, and older interactive-report outputs

### 2. Nevada suppression guidance

- https://nevadareportcard.nv.gov/DI/MoreDownload?filename=DATA+SUPPRESSION+GUIDELINES+FOR+PORTAL.pdf

### 3. Nevada ACGR guidance

Useful for understanding comparable numerator rules across years, especially diploma types.

- https://nevadareportcard.nv.gov/DI/MoreDownload?filename=Adjusted+Cohort+Graduation+Rate+Data+Validations+Guidance+for+4+year+class+of+24-25.pdf

### 4. Charter-school universe / sponsor source

Use this to identify which schools belong in the charter sector and which sponsor they sit under.

- Charter overview and sponsor links: https://doe.nv.gov/charter-schools/
- School and district directory landing page: https://doe.nv.gov/school-and-district-information

These sources should be paired with legacy accountability reports and sponsor documents when a school's legal status is ambiguous in older years.

### 4b. Grade-12 presence cross-check source

When a school-year remains unresolved, especially for expanding schools, renamed schools, transition schools, or schools that may not yet have had a graduating cohort, cross-check against Nevada's annual enrollment-by-grade spreadsheets.

Recommended use:

- confirm whether the school had any 12th-grade enrollment in the relevant school year
- use that finding to distinguish between a real high-school universe row with missing ACGR detail and a school-year that likely had no graduating cohort yet
- when the grade-by-grade file shows no 12th-grade enrollment, treat that as affirmative evidence that the school-year should be excluded from the four-year graduation universe unless a contrary published ACGR row exists
- do not let this override a published ACGR row, but do use it to tighten hold decisions where the graduation files are ambiguous

Important caveat:

- the October enrollment snapshot and the four-year adjusted cohort are not identical concepts, so a published ACGR row can still exist even when the current-year enrollment workbook shows no 12th graders
- `Southern Nevada Trades High School` in the Class of 2024-25 is a concrete example in the current build: the official annual ACGR PDF publishes a school-level rate, so that published row controls even though the 2024-2025 enrollment workbook does not show a grade 12 row for the same entity

### 5. SPCSA context / category source

SPCSA publishes sector context and explicitly separates some discussion by school model.

- SPCSA academic framework reports landing page: https://charterschools.nv.gov/Performance_Reports/SPCSA_Academic_Framework_Reports/
- 2017-18 SPCSA annual report card: https://charterschools.nv.gov/uploadedFiles/CharterSchoolsnvgov/content/Grocers/230127-Final-2017-18-SPCSA-Annual-Report-Card-18-E.pdf
- State of the SPCSA 2024 deck: https://charterschools.nv.gov/uploadedFiles/CharterSchoolsnvgov/content/News/2024/2024_01_26_StateofSPCSA.2024_Final.pdf
- SPCSA Class of 2021-22 attachment: https://charterschools.nv.gov/uploadedFiles/CharterSchoolsnvgov/content/News/2022/20221216_SPCSA_GradRatesPresentation_ATTACHMENT.pdf
- SPCSA Class of 2022-23 attachment: https://charterschools.nv.gov/uploadedFiles/CharterSchoolsnvgov/content/News/2023/20231208_SPCSA_GradRatesPresentation_ATTACHMENT.pdf

## What The Nevada Files Give You

For each year, the Nevada ACGR PDF gives you:

- statewide counts and statewide rates
- district / sponsor rates
- school-level overall ACGR
- school-level subgroup ACGRs

Important limitation:

- the school-level tables generally publish rates, but not school-level cohort counts or school-level graduate counts

That means a simple average of school rates is not valid for a sector-wide estimate. You need a weighting strategy.

Promising supplemental source:

- the Nevada Accountability Portal interactive cohort report appears to expose school-level graduation rates and some completion counts for later years, which may help with school-level weighting recovery where the PDFs are insufficient

## Recommended Sector Calculation Approach

### Preferred rate to publish

Publish a weighted sector estimate:

`sector ACGR = sum(estimated graduates across charter schools) / sum(estimated cohort across charter schools)`

### Best practical weighting hierarchy

Use this hierarchy in order:

1. If you can obtain school-level cohort counts from a second public source, use those directly.
2. If you can obtain school-level graduate counts from accountability report cards or completion-indicator tables, back-calculate cohort as `graduates / rate`.
3. If neither is available for a school-year, publish a bounded estimate instead of a false exact number.

### Why this is still defensible

Your output is explicitly an estimate, not a recreated official NDE rate. The goal is to estimate the charter sector consistently across years and sponsors using public data, while being honest about where Nevada's publication rules limit exact replication.

## Handling Suppression And Coding

Nevada's public rules matter a lot here.

From the suppression guidance:

- counts below 10 are suppressed
- 0 is not suppressed
- percentages below 5 are bottom-coded
- percentages above 95 are top-coded

### Recommended treatment for school overall rates

For the school-level overall ACGR field:

- exact numeric rate, for example `83.8`: use as published
- `+`: treat as an interval from `95.0` to `100.0`
- `*`: treat as an interval from `0.0` to `5.0`
- `NA`: exclude from the sector denominator for that year unless you have evidence a valid cohort existed

### Recommended estimation rule

For any top/bottom-coded school, calculate:

- low estimate using `95.0` for `+` and `0.0` for `*`
- midpoint estimate using `97.5` for `+` and `2.5` for `*`
- high estimate using `100.0` for `+` and `5.0` for `*`

Then publish:

- point estimate = midpoint
- uncertainty band = low to high

This is much better than pretending `+` means `95` or `100` exactly.

### Smoothing rule recommendation

If you need a single-value smoothing assumption for charting or back-of-the-envelope aggregation, the most defensible rule is to use the midpoint of Nevada's public interval rather than an arbitrary fixed number:

- `+` or `>95.0` becomes `97.5`
- `*` or `<5.0` becomes `2.5`

Why this is more defensible:

- it matches the midpoint of the public interval implied by Nevada's own disclosure rules
- it is symmetric and easy to explain
- it does not assume unusually strong or weak performance within the masked range

Less defensible approaches:

- treating all `+` values as `95.0`
- treating all `+` values as `100.0`
- assigning an arbitrary number such as `97.0` without tying it to the public interval

Important caution:

- if the issue is a suppressed small cohort count rather than just a masked rate, do not replace every unreported count with a fixed `n<10 = X` assumption unless you are explicit that this is a modeling convenience rather than a recovery of the underlying data
- for final reporting, prefer a midpoint estimate plus a low-high band whenever possible

### First graduating class rule

Do not exclude a school-year just because it represents a school's first graduating class.

Use this rule instead:

- if Nevada publicly reports a numeric rate, a top-coded rate, a bottom-coded rate, or another usable interval-coded result for that first graduating class, count it
- if Nevada reports the school-year as `N/A`, `no prior graduating class`, or otherwise provides no usable public rate, keep the school in the universe but hold that row out of exact aggregation unless another defensible public value can be recovered

Why:

- a first graduating class can still reveal real school performance and real data-quality problems
- excluding all first graduating classes would risk biasing the sector upward by screening out difficult or poorly managed launch years
- the honest dividing line is data availability, not whether the cohort was the first one

## Source Hierarchy And Crosswalk Note

Use this hierarchy when there are multiple public versions of a rate:

1. Official Nevada Department of Education / Nevada Accountability Portal annual ACGR file
2. SPCSA attachment that explicitly states the rates are from NDE ACGR records
3. SPCSA presentation deck or summary slide

Recommended note for the file and any future memo:

"Where available, official Nevada Department of Education ACGR files are treated as the controlling public record. SPCSA presentations and attachments are used as secondary sources for school-level charter detail, crosswalk support, or model-specific context. Some SPCSA materials restate NDE values after truncation, rounding, school-name shortening, or portfolio-specific formatting, so small differences between SPCSA-published tables and the official NDE release should be expected and do not necessarily indicate a substantive discrepancy."

This matters because SPCSA materials sometimes:

- truncate values to one decimal place
- round privacy-protected n-sizes
- shorten school names
- display `>95.0` / `<5.0` style codes rather than the exact public number shown elsewhere

When challenged, the safest position is:

- use NDE as the official public record
- use SPCSA as a documented derivative source
- disclose when a school-year value came from an SPCSA attachment instead of directly from the NDE annual PDF

Recent example from the current build:

- in the Class of 2024-25 recovery, the official NDE annual ACGR PDF was used to add `Explore Academy` and to recover `NSHS Meadowwood` because those school-level rows were visible in the NDE file even though the working SPCSA deck did not function as a complete one-to-one school census for the year
- that is exactly the kind of case where the NDE annual file should control the universe and the school-level reported value
- the same cross-check also clarified that `Explore Academy` had no 12th-grade enrollment in `2022-23`, then appeared as a reportable ACGR row in `2023-24`, which is a good reminder that a school can exist as a high school program before it actually enters the four-year graduation universe
- later recovery also added `Thrive Point Academy` as an SPCSA alternative / APF school and clarified that newer schools such as `CIVICA Academy`, `CASLV Cadence`, and `Young Women's Leadership Academy of Las Vegas` can appear in statewide school ratings and enrollment files before they become countable graduation-universe schools

### Beacon-specific note

Recommended language:

"Beginning with Beacon Academy's transition to an exclusively alternative education mission in December 2016, Beacon should not be treated as directly comparable to traditional open-enrollment charter high schools. SPCSA records indicate that Beacon crossed the eligibility threshold for Nevada's Alternative Performance Framework and began operating under that framework in 2018-19. For sector reporting, Beacon is therefore best presented as a separate reported entity or, at minimum, isolated from brick-and-mortar charter trend lines."

### Alternative-framework context

Nevada's APF guidance says a charter school is eligible for APF rating if its mission is to primarily serve qualifying students and at least 75% of enrolled students meet one or more statutory eligibility criteria, including being academically disadvantaged, expelled or suspended, adjudicated, or having an IEP.

Current working interpretation for this project:

- Beacon Academy is the only SPCSA high school that is clearly documented in the public record as operating under the Nevada Alternative Performance Framework during most of the period we are studying.
- There is also public evidence that The Delta Academy, a Clark County School District-sponsored charter, was additionally rated on the APF starting in 2021-22.
- A Nevada APF school list dated October 20, 2025 shows Thrive Point Academy approved under the APF for SY2024-25 and Beacon Academy approved under the APF for SY2018-19.
- That same APF list includes Washoe Inspire Academy, Marvin Picollo School, and Turning Point under Washoe County School District, but does not list enCompass Academy.

Because of that, do not assume every school that markets itself as serving at-risk or credit-deficient students is formally comparable to Beacon for accountability purposes.

### Washoe caution note

Recommended language:

"Some Washoe-sponsored charter high schools may have served students with alternative-education characteristics, but absent public verification that they were formally approved to operate under the Nevada Alternative Performance Framework, they should not be assumed to be accountability-equivalent to Beacon."

### enCompass note

Current working interpretation:

- enCompass Academy appears to be the relevant Washoe-sponsored charter high school to watch in this category.
- Washoe public materials show the school operating as `enCompass Academy Charter HS (9-12)` and indicate a charter renewal date of July 1, 2018.
- A Nevada APF school list dated October 20, 2025 does not include enCompass Academy, which weighs against treating it as a formally APF-approved alternative charter school.

Recommended handling:

- keep enCompass in the working alternative / turnaround watchlist
- do not classify it as formally APF-equivalent unless we find a public source showing approval under the Nevada Alternative Performance Framework

### Why Washoe is harder

Washoe is more challenging mainly because of school identification and crosswalk issues, not because the Nevada graduation files are unusable.

- The annual NDE ACGR PDFs do report Washoe charter schools, including `Coral Academy High School`, `Academy For Career Education`, and `enCompass Academy`.
- The harder part is matching those annual reporting names back to a stable charter-school universe across time.
- Washoe schools show more naming variation and lineage ambiguity than SPCSA. Examples include `Rainshadow CCHS` later appearing as `enCompass Academy`, `ICDA Charter HS` appearing as `I Can Do Anything Charter`, and some schools carrying slightly different high-school labels across sources.
- That means the main methodological risk is not suppression by itself. It is accidentally double-counting, missing, or misclassifying a school when names, grade spans, or school missions shifted.
- Suppression still matters, but it is secondary. Once the school identity is pinned down, Nevada's top-coded and bottom-coded rows can still be used through low-mid-high interval treatment.

## Achievement School District Wrinkle

Nevada had a separate statewide charter authorizer, the Achievement School District, during the mid-to-late 2010s.

Current working interpretation:

- 2015 Nevada legislation established the Achievement School District within the Nevada Department of Education for conversion of certain underperforming schools to achievement charter schools
- 2019 Nevada legislation abolished the Achievement School District and directed existing ASD schools and approved applicants toward SPCSA sponsorship
- the class of 2019-20 annual ACGR comparison table still reports `Achievement School District` as its own public comparison row

Practical handling rule:

- keep ASD visible as its own historical official comparator when NDE reports it separately
- do not automatically merge historical ASD rows into SPCSA for descriptive trend tables without saying so explicitly
- at the school level, verify whether an ASD school actually had a graduating cohort before assuming it belongs in the high-school ACGR universe
- for pre-July 2019 ASD materials, inspect whether the reporting table is using an ASD school name as both the LEA label and the campus label before counting rows; do not let that legacy formatting create a false duplicate school

Important caution:

- ASD-era school-level rows should be kept under `Achievement School District` for the years in which that was the actual public authorizer, even if later SPCSA materials restate the school under a successor name
- `Democracy Prep at Agassi High` is now recovered as a usable ASD-era school row in the official `2017-18` and `2018-19` ACGR files and should not be back-cast into SPCSA for those years
- the user has flagged an additional structural issue that fits the public record: before the July 3, 2019 transition, ASD schools were treated as their own LEAs, so some 2015-17 style tables may place the school name in the LEA column as well as the campus column

Legacy crosswalk rule:

- when auditing 2015-17 ASD-era files, treat LEA name, campus name, and campus code as separate fields that must be reconciled before counting schools
- if a row appears to show the same ASD school in both the LEA and school column, treat it as a formatting or governance artifact first, not evidence of two entities

## Accountability Transition Wrinkle

The 2015 through roughly 2018 period needs extra caution for accountability comparability.

What is clear from the public record:

- Nevada shifted to Smarter Balanced aligned accountability during this period
- the 2016-17 NSPF guideline and 2017-18 NSPF manual reflect a still-evolving ESSA-era accountability system
- Nevada's published accountability materials note that the state would report as much as it could as data became available until pooled averaging and related measures stabilized

Working interpretation for this project:

- the user's recollection that the early SBAC and vendor-transition years disrupted smooth school-level comparability is directionally consistent with the public record
- the exact first year that multi-site charter campuses became fully comparable school by school still needs source-by-source verification
- until that is locked down, treat `2019` school-level or campus-level comparisons as especially valuable but do not overstate them as the single definitive first year without a confirming source

### What to do with suppressed subgroup cells

For subgroup tables, do not impute aggressively unless subgroup analysis is the main purpose. For public reporting:

- keep subgroup cells as missing when NDE suppresses them
- only use subgroup data for descriptive context, not for constructing the main sector total

That avoids compounding error from multiple imputed cells.

## Recommended School Classification Scheme

Build a yearly school master file with these fields:

- year
- sponsor
- district
- entity_id
- school_name
- charter_flag
- charter_authorizer
- model_type
- include_in_sector_total
- notes

For the current build, that function is split across:

- `nevada_charter_universe_audit.csv` for school-level legal-status screening and authorizer history
- `nevada_charter_legacy_universe_2015_16_to_2019_20.csv` for the high-risk legacy years where inclusion, exclusion, and crosswalk holds need to be explicit by school-year
- `nevada_charter_school_year_panel.csv` for the broader school-year ACGR working panel
- `nevada_charter_panel_decisions.csv` for a unified school-year decision layer that converts the audit and panel evidence into actual count / hold / no treatment
- `nevada_charter_panel_decision_summary.csv` for a quick by-year snapshot of how many school-years are currently counted versus still held
- `nevada_charter_sector_trend_table.csv` as the output layer rebuilt from the official comparison series plus the decision ledger rather than from ad hoc row-by-row notes
- the publishable output now also includes separate SPCSA lines for `Nevada Connections`, `Nevada Virtual`, and `Leadership Academy` so the online and online-adjacent schools do not only appear inside one aggregate virtual slice

## Best Next Historical Source

For the pre-`2017-18` school-by-school graduation recovery, the best next public source is likely the Nevada Report Card student interface rather than only the later annual PDF archive:

- `https://nevadareportcard.nv.gov/di/main/students`

The Nevada Report Card FAQ says the portal provides state, district, and school-level data going back to 2003, including high school graduation rates. That makes the interactive student section a stronger candidate for recovering older school-specific rows from `2013-14` through `2016-17` than relying only on the newer annual ACGR comparison PDFs.

Working implication:

- keep the official early-year sponsor totals already shown in the output tables
- treat the next historical build step as a direct portal extraction task from the Nevada Report Card student interface
- use that interface first for older school-level charter rows before assuming the rows are unavailable
- `nevada_grade12_enrollment_crosscheck_sources.csv` for the official NDE annual enrollment-by-grade spreadsheet links
- `nevada_grade12_crosscheck_tracker.csv` for the school-years where checking 12th-grade enrollment is most likely to resolve a hold or confirm that a school belonged in the graduation-rate universe

The portal recovery has now materially improved the early SPCSA years:

- direct Nevada Report Card queries now backfill a meaningful `2013-14` through `2016-17` SPCSA school layer rather than leaving those years at sponsor-total only
- the same portal workflow, together with downloaded multi-year exports, now backfills early district-authorized charter rows for Clark and Washoe through `2016-17`, which materially improves the early district charter totals even though the early district drilldowns are still thinner than the SPCSA side
- the downloaded multi-year export shows Davidson as school-level rows under entity `19406` and later `84406`, but it does not expose a separate visible `University Schools` aggregate row; that means the export is useful for excluding Davidson from charter slices, while unresolved questions about historical sponsor-total contamination should remain explicit caveats rather than be treated as resolved
- `Independence` and the correctional LEA context should be handled the same way: if a school-level row is visible, it stays outside every charter slice, and if an official historical sponsor total may have absorbed it, that possibility should be disclosed as a comparator caveat rather than silently carried into the charter estimate
- confirmed usable legacy rows now include `Alpine`, `Beacon`, `Nevada Connections`, `Nevada Virtual`, `Quest`, the pre-campus-split `Nevada State High School`, and the `Silver State` / `Argent` lineage, with `Coral Academy of Science Las Vegas` visible beginning in `2014-15`
- the pre-campus-split `Nevada State High School` should be treated as its own legacy entity before later campus breakout years rather than back-cast into one later campus
- `Quest Academy` is visible in the historic public portal but still lacks a clean later crosswalk, so it should remain a legacy SPCSA entity unless stronger successor evidence emerges

## Replication Workflow

Researchers should be able to recreate the current public outputs by following this sequence:

1. Download the official Nevada annual 4-year ACGR PDFs for every year in scope.
2. Record the official statewide, SPCSA, ASD where applicable, Clark, Washoe, and Carson public comparator rates directly from those files.
3. Recover school-level charter rows from the same annual PDFs where available, then use Nevada Report Card portal queries and downloaded multi-year exports to backfill legacy school-level rows.
4. Normalize the school-year universe by entity ID first and school name second so transitions such as `Rainshadow` / `enCompass`, `Silver State` / `Argent`, and pre-split / post-split `Nevada State High School` rows are handled consistently.
5. Exclude non-charter entities from all charter slices, including district option schools and non-charter statewide entities such as `Davidson` and `Independence`, even if they may have appeared in historical public sponsor aggregations.
6. Use Nevada's grade-by-grade enrollment spreadsheets to test unresolved school-years for actual 12th-grade presence.
7. Apply the project decision rule to each school-year:
   - `count` when a usable public ACGR value exists
   - `hold` when the school belongs in the graduation universe but no usable public rate can yet be recovered
   - `exclude` when the school was not a charter high school in that reporting year or had no 12th-grade graduation-universe basis
8. Apply interval treatment to suppressed or coded values using the project's low-mid-high convention:
   - `+` -> `95.0 / 97.5 / 100.0`
   - `*` -> `0.0 / 2.5 / 5.0`
9. Generate official public comparator rows separately from estimated charter slices so historical contamination questions, if any, remain transparent rather than being silently baked into the estimates.
10. Rebuild the final trend tables from the decision ledger and school-year panel rather than hand-editing summary outputs.

The practical implication is important: this project reproduces official public sponsor totals as published, but it independently estimates charter-only subgroup slices from a screened school universe. That is why `Davidson`, `Independence`, and similar non-charter entities are excluded from the charter estimates even where the historical official sponsor totals may still deserve caution notes.

### Official SPCSA vs adjusted SPCSA

The public outputs should now show two distinct SPCSA lines:

- `SPCSA official public`: the sponsor-level rate published by Nevada
- `SPCSA adjusted charter-only`: the screened charter-only estimate built from counted SPCSA charter school rows after excluding non-charter entities such as `Davidson` and `Independence`

This is an analytic sensitivity step, not a claim that Nevada's official historical sponsor total was formally corrected or proven wrong. The point is to isolate the charter portfolio without overwriting the historical public record.

Interpretation note:

- the adjusted line is especially useful in the earlier years, when mixed-entity public reporting appears more plausible
- by roughly `2018-19` forward, the public files look materially cleaner, so any remaining official-versus-adjusted gap should be interpreted more as a difference between sponsor-total reporting and school-level screened estimation than as proof of a continuing aggregation defect

### Authorizer buckets

Use:

- `SPCSA`
- `Clark district-sponsored charter`
- `Washoe district-sponsored charter`
- `Carson district-sponsored charter`
- `other authorized charter`, if one appears in later years

Important historical note:

- for class years before the 2025-26 school year, keep the authorizer that actually sponsored the school in that reporting year
- do not retroactively relabel historical CCSD-sponsored schools as SPCSA schools just because sponsorship changed later

Current-authorizer note:

- SPCSA's 2026 Growth Management Plan says six CCSD charter schools transferred to SPCSA sponsorship effective July 1, 2025
- that change matters for current governance and future reporting, but it should not rewrite the historical authorizer attached to pre-transfer graduation-rate years

### Model-type buckets

Use:

- `brick_and_mortar`
- `statewide_online`
- `alternative`

If a school changes model over time, treat classification as year-specific, not permanent.

### Special breakout recommendation

Beacon Academy should generally be reported separately from the rest of the charter alternative-school group.

Why:

- SPCSA records indicate Beacon transitioned to an exclusively alternative education program in December 2016.
- SPCSA later documented that Beacon crossed the eligibility threshold for Nevada's Alternative Performance Framework and began operating under that framework in 2018-19.
- Beacon serves a population that is overwhelmingly over-age, under-credit, previously dropped out, chronically absent, or otherwise eligible under Nevada's alternative-school criteria.

Recommended presentation:

1. All charter high schools
2. Charter brick-and-mortar excluding Beacon
3. Statewide online charters
4. Beacon Academy
5. Optional: other alternative charters

This avoids allowing Beacon's very different mission and eligibility rules to distort comparisons with traditional charter high schools.

### Presentation recommendation

Always publish at least these three trend lines:

1. All charter high schools
2. Charter brick-and-mortar only
3. Charter statewide online only

If the alternative-school population is material, publish it separately rather than folding it silently into brick-and-mortar.

## Practical Calculation Workflow

### Step 1. Build the school universe

For each year:

1. Pull all charter high schools from NDE directory / sponsor lists.
2. Assign sponsor and model type.
3. Keep a note for openings, closures, reconstitutions, and name changes.

### Step 2. Pull annual ACGR school rates

From each annual Nevada ACGR PDF, capture:

- year
- district / sponsor
- school name
- entity_id
- overall graduation rate

### Step 3. Attach a weighting field

Preferred:

- school-level all-student cohort count

Fallback:

- estimated cohort from graduates divided by rate

Last-resort fallback:

- publish only sponsor/model averages with a clear note that no defensible sector weighting field was publicly available for that year

Current practical fallback now in use for the first trend-table draft:

- when an official sponsor total is publicly available, use that sponsor total directly for the `total` row
- when only school-level model breakout rates are available and school-level cohort weights are still missing, calculate provisional `brick-and-mortar`, `virtual`, `Beacon`, or similar slices as simple averages of the verified school-level midpoint, low, and high values
- label those breakout values explicitly as provisional unweighted school averages, not recreated NDE weighted sector totals

### Step 4. Calculate three versions

For each year and each sector slice, calculate:

- low estimate
- midpoint estimate
- high estimate

This produces a credible range around the charter-sector rate.

### Step 5. Check against sponsor totals

Use the published sponsor-level rates as a reasonableness check:

- SPCSA sponsor rate in the Nevada annual file
- district report-card charter sections where available

If your rolled-up SPCSA estimate is wildly different from the published SPCSA rate, that is a sign the school universe or weights need review.

## Comparability Notes By Year

These should be disclosed in any chart notes.

### Class of 2017-18 onward

Nevada ACGR guidance says the College and Career Ready Diploma is counted beginning in school year 2017-18.

### Class of 2018-19 onward

Nevada ACGR guidance says the Alternative Diploma is counted beginning in school year 2018-19.

### Class of 2023-24 onward

Nevada states that published ACGR values are truncated beginning with the Class of 2023-24.

Implication:

- pre-2023-24 and post-2023-24 values are still comparable at a high level
- but back-calculating counts from rates becomes a bit less precise starting in 2023-24

## How To Present The Results

### Main table

Use one row per year with these columns:

- class year
- charter sector estimated ACGR midpoint
- low estimate
- high estimate
- estimated cohort covered
- number of charter high schools
- notes

### Secondary table

Break out by sector slice:

- all charters
- brick-and-mortar
- statewide online
- alternative
- SPCSA only
- district-sponsored only

Important presentation note:

- in the current build stage, `SPCSA total` may be an official public sponsor rate while `SPCSA brick-and-mortar` and `SPCSA virtual` are provisional school-level averages
- those numbers are still useful together, but they should not be described as if they were all produced by the same weighting method

### Charts

Use:

1. Line chart for trend over time
2. Clustered bars for year-by-year comparison of brick-and-mortar vs online vs alternative
3. Optional ribbon or error-bar overlay to show suppression-driven uncertainty

### Chart note template

"Rates are estimated from Nevada public school-level ACGR files. Publicly suppressed and top/bottom-coded values were converted into bounded intervals, so each annual estimate is shown as a midpoint with a low-high range."

## Recommended Minimum Disclosure Language

Use something close to this:

"This analysis estimates Nevada's charter-sector 4-year adjusted cohort graduation rate by aggregating school-level public data across SPCSA- and district-authorized charter high schools. Because Nevada publicly suppresses some small cells and top/bottom-codes extreme values, sector totals should be interpreted as estimates rather than exact replications of NDE's internal calculations."

## Best Next Step

If you want to operationalize this quickly, build a single workbook or csv with one row per school-year and the fields listed above, then calculate:

- all-charter weighted midpoint, low, and high
- brick-and-mortar midpoint, low, and high
- online midpoint, low, and high
- alternative midpoint, low, and high

That gives you one defensible core output and two or three decision-useful breakouts.

## Working Files In This Folder

This workspace now includes:

- `nevada_charter_grad_rate_sources.csv`
- `nevada_charter_high_school_master_seed.csv`
- `nevada_charter_school_year_panel.csv`
- `nevada_charter_grad_rate_template.csv`
- `nevada_charter_comparison_framework.csv`
- `nevada_charter_official_comparison_series.csv`
- `nevada_charter_sector_trend_table.csv`

Important caveat:

- the `master_seed` file is a verified starting list based on schools visible in recent graduation-rate materials, not yet a final year-by-year census
- some entity IDs and model classifications, especially for older Washoe schools and some SPCSA alternative schools, still need directory-level validation

### Panel workflow fields

The `nevada_charter_school_year_panel.csv` file currently expands the seed list across Class of 2017-18 through Class of 2024-25 and uses these working fields:

- `reported_as_high_school`: whether the school has been verified as part of the charter high-school universe for that class year
- `acgr_row_present`: whether the school has been verified as appearing in the relevant graduation-rate reporting material for that class year
- `published_rate_status`: whether the public rate is numeric, top-coded, bottom-coded, unavailable, or still unchecked

Current working values:

- `yes`: verified
- `unchecked`: not yet verified for that exact year
- `numeric`: public rate entered as a numeric value
- `topcoded`: public rate shown as `+`
- `topcoded_exact_shown`: source displays `100.0`, but the estimation workflow still treats this as bounded because the broader publication rules top-code extreme values
- `small_n_unreported`: source indicates the cohort was under the public minimum n-size threshold, for example `n<10`
- `no_prior_graduating_class`: source indicates the school did not yet have a comparable prior graduating class, or marks the rate as `N/A` in a change table

Recommended handling:

- `small_n_unreported` does not mean the school should vanish from the universe; it means the school-year belongs in the universe but may need interval treatment or a hold depending on whether a usable public rate is still visible elsewhere
- `no_prior_graduating_class` should not be used as a blanket reason to exclude all early cohorts; it is only a hold status when the public source truly provides no usable rate for that school-year

This is intentionally conservative. The panel is meant to support year-by-year verification and data entry without assuming that every school operated in every year.

### Current data-entry progress

As of this draft:

- the comparison framework now explicitly distinguishes statewide, all-district official public rates, and separate official public comparator rows for SPCSA, Clark, Washoe, and Carson
- the comparison framework now explicitly distinguishes statewide, all-district official public rates, and separate official public comparator rows for SPCSA, ASD where applicable, Clark, Washoe, and Carson
- a new `nevada_charter_official_comparison_series.csv` file carries the official comparison spine for class years 2013-14 through 2024-25, with legacy-year coverage notes where recovery is partial or based on older accountability materials
- a new `nevada_charter_sector_trend_table.csv` file preloads those official comparator rows into the final output shape that will later receive the estimated charter slices
- 2017-18 SPCSA school-level rows recoverable from the official SPCSA annual report card have been entered for Alpine, Argent, Beacon, Nevada Connections, Nevada Virtual, and Oasis
- 2023-24 district-authorized Clark charter high schools from the annual Nevada ACGR file have been entered where verified from the cited source
- Clark district-authorized charter high-school rows now extend into multiple modern years, which is enough to support provisional multi-year Clark charter slices in the trend table
- Clark district-authorized charter rows now extend across multiple modern years for the brick-and-mortar charter schools and Delta, but they do not currently include a verified Clark-sponsored charter virtual row
- Washoe district-authorized charter rows now include verified annual ACGR entries for Coral Academy High School, Academy for Career Education, entity 16610 appearing as enCompass Academy, and older ICDA rows across the annual ACGR files, but the Washoe charter slice is still materially less stable than SPCSA because the legacy school crosswalk is more fragile
- 2022-23 SPCSA high-school rows visible in the SPCSA attachment have been entered with midpoint, low, and high estimate fields
- 2021-22 SPCSA high-school rows visible in the SPCSA attachment have been entered with midpoint, low, and high estimate fields
- 2020-21 SPCSA high-school rows have been entered from the SPCSA final deck for the class of 2021
- 2019-20 SPCSA high-school rows and most 2018-19 SPCSA rows have been entered from the SPCSA final deck for the class of 2020
- pre-2017-18 legacy classes are still awaiting source-by-source recovery and crosswalk work before the panel is extended further backward
- remaining years and schools are still awaiting year-by-year verification and value entry
