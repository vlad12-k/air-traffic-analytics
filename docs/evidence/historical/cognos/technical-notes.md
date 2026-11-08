# Historical IBM Cognos — technical walkthrough of all eight original archive screenshots

The current working-tree gallery links all eight original Cognos PNGs, but that inventory is not a rights or accuracy clearance. The owner identifies the reports/model as authored work; this does not license embedded data, maps, or vendor content. See the [per-image release inventory](../../screenshot-release-inventory.md): the semantic-model view is a non-data candidate, global-value views are held for AVI0301/ICAO rights, the demand pages have a period-label mismatch, and operational pages need field-level lineage confirmation.[2][3] Cognos UI alone is not an exclusion reason. No original screenshot is changed here, and no current Cognos deployment or refresh is claimed.

The sequence follows the historical workflow: inspect the semantic model → review UK airport demand and recovery → explore executive and operational pages → inspect risk-ranking evidence.

## 1. Semantic model — historical data module

![Original IBM Cognos Analytics semantic-model screenshot](historical-cognos-07-semantic-model.png)

**Business purpose.** Provide a reusable analytical layer for the airport screening and reporting workflow rather than defining every report page against unstructured source extracts.

**What the screenshot evidences.** The visible Cognos data-module object list includes GT-named tables such as `GT1_UK_Airport_Yearly_Totals`, `GT2_UK_Airport_YoY_Growth`, `GT3_Top10_UK_Airports_By_Intl`, `GT4_Top10_Routes_By_DestCountry`, `GT6_Post_Covid_Recovery`, `GT8_Intl_Share_vs_Routes`, `GT9_KPI_Summary`, `GT7_Global_Expansion_Candidates`, and `GT10_LWC_Recommendation`. A Relationships area and diagram settings are also visible. This documents the historical BI model's object vocabulary and a relationship-design workspace.

**Model interpretation.** The later public V2 contract set defines GT1–GT10 grains and semantics, including one row per airport in GT1/GT3, airport × destination country in GT4, run × KPI in GT9, and candidate × scope × scenario × model version in GT10. These contracts provide current project documentation, but they do not prove that the historical Cognos module used exactly the same keys, joins, calculations, or final grain. The screenshot does not make individual cardinalities or filter directions legible enough to assert them.

**Decision supported.** A governed model structure can support consistent airport demand, destination, quality, and recommendation reporting. This image is evidence of model authoring context, not proof of model correctness or deployment.

**Validation and limits.** Current Python/SQL V2 documents reconciliation and quality gates and a recorded canonical run with 30 checks, zero failures, and zero warnings. That is not a validation of the historical Cognos module. No Cognos package, query definitions, or runnable source data are part of this public repository. IBM UI is visible; no IBM permission or endorsement is claimed.

## 2. UK demand filter — historical decision-pack view

![Original IBM Cognos Analytics UK demand-filter screenshot](historical-cognos-11-demand-filter.png)

**Business question.** How do the represented UK airports compare on passenger scale, and what does the selected airport's displayed period comparison suggest for the first-site screen?

**What the screenshot evidences.** The visible report is titled “UK decision pack (Top 10 UK airports, 2022)” and shows an airport list/filter with Heathrow selected. It includes total passengers, average monthly passengers, a top-airport ranking, and period-comparison/growth views. The screenshot labels the prior period 2020, which conflicts with the official CAA comparison period; no numeric figures are transcribed here.[4][12]

**Model and filters.** The report is an interactive Cognos page with a UK airport selection and top-10 presentation. The source inventory and local reconciliation associate its current/prior airport passenger pairs with UK CAA Table 12.1, source period 202205 and its supplied prior period. The screenshot labels the periods 2022 versus 2020, but the official Table 12.1 comparison is May 2022 versus May 2021; the image itself is not corrected and is held from recruiter-facing reuse until this mismatch is resolved.[4][12] The preserved GT1 output provides the same two-period airport comparison. This is not a continuous annual time series. The original Cognos query, field mapping, joins and refresh remain unavailable; other page calculations should not be inferred from the GT1 match.

**Interpretation and decision.** The page communicates Heathrow's leading displayed 2022 passenger total and a substantial historical recovery multiple, supporting further investigation of Heathrow in the historical decision pack. Recovery in airport passenger totals is not retail footfall, and the ratio is not a sales forecast.

**Validation and limitations.** No historical Cognos query, source-row extract, or independent Cognos recalculation is included. A separate local cross-check compared the ten displayed airport current/prior totals with the preserved GT1 output derived from CAA Table 12.1; all ten airport rows matched. This corroborates the source association but does not recover the original Cognos query or prove the report’s refresh path. The current V2 pipeline's recorded quality run does not validate this historical report. CAA attribution/no-resale conditions apply.[4] IBM UI is visible; no IBM endorsement or separate permission letter is claimed.

## 3. UK demand recovery — historical two-period comparison

![Original IBM Cognos UK airport demand-recovery report](historical-cognos-10-demand-recovery-original.png)

**Business question.** How do the ten represented UK airports compare on current and prior passenger totals, and how does the selected airport’s recovery ratio compare with its market position?

**What the screenshot shows.** The original report contains a UK airport selector and top-airport list, current/prior period passenger totals, average-monthly context, a recovery multiple, and monthly share views. Heathrow is selected; the screenshot labels the periods 2020 and 2022, but the official source comparison is May 2022 vs May 2021. No screenshot values are transcribed as period-correct numerical results here.[4][12]

**Source and model cross-check.** A local comparison checked the ten displayed airport labels and all ten current/prior passenger pairs against `outputs/golden/GT1_UK_Airport_Period_Totals.csv`; all ten rows matched. That canonical GT1 output is derived from UK CAA Table 12.1, May 2022 vs May 2021.[4][12] This is strong source corroboration for the displayed table but not proof of the original Cognos query, ETL, relationship path, refresh or calculation implementation. Current V2 counterparts are [`golden.py`](../../../../src/airtraffic/golden.py), [GT1–GT2 contracts](../../../gt-contracts.md), and `sql/validation_queries.sql`; they are explanatory reference, not a retroactive Cognos test.

**Decision, validation and limits.** The page supports further UK-site diligence by showing passenger-market scale and a period comparison, but its period label conflicts with the official CAA comparison.[12] It does not measure retail footfall, forecast sales, or prove profitability. CAA attribution and no-sale/no-resale conditions apply; the underlying CSV remains local.[4] The original remains unchanged in the current gallery but is held from recruiter-facing reuse pending an approved correction/context. IBM Cognos UI is visible; no IBM endorsement or separate permission letter is claimed.

## Additional five original Cognos archive pages — complete gallery

The five additional originals are shown below with technical context. The owner authorizes publication; the descriptions avoid claiming that current Python/SQL code reproduces the historical Cognos query or scoring logic.

### 4. Executive summary — combined UK and global decision pack

![Original IBM Cognos executive summary](historical-cognos-08-executive-summary-original.png)

The page brings together a UK airport ranking/demand view, a global airport ranking/map, an SFO historical benchmark, and a COVID-recovery panel. It is designed as a leadership overview for comparing market scale and recovery signals before drilling into airport detail. The dashboard layout suggests coordinated filters, but a PNG cannot verify which visuals cross-filter or what query/model relationships drive them.

The global airport ranking uses AVI0301/ICAO-linked values according to the project source inventory.[2][3] The original remains unchanged in the current working-tree gallery, but is held from further release pending rights confirmation; no cropped or reconstructed replacement is used. Current V2 mappings for UK totals, CAA/route measures and SFO context are in [`golden.py`](../../../../src/airtraffic/golden.py) and the [GT contracts](../../../gt-contracts.md); these do not establish the historic Cognos source joins or independently validate the displayed values.

### 5. Executive summary filter — selected-airport interaction

![Original IBM Cognos executive-filter state](historical-cognos-09-executive-filter-original.png)

This second executive page captures a selected-airport state within the global executive dashboard. The selector changes the highlighted airport and the selected-city passenger KPI while the map and top-airport comparisons remain on the page. It demonstrates the intended interaction state, not the Cognos filter expression, join path, or runtime filter propagation.

The page contains AVI0301-linked global values and a global airport map.[2][3] The original remains in the working-tree gallery but is held from further release pending source-rights and map-attribution review; no numeric values are repeated in this note. The underlying model/data-module package and report specification are absent; the current V2 model is not offered as proof of the Cognos implementation.

### 6. Operational monitoring — multi-airport dashboard

![Original IBM Cognos operational-monitoring report](historical-cognos-12-operational-monitoring-original.png)

This page combines an airport selector, KPI cards, a passenger-versus-recovery view, an operational-risk treemap, an airport comparison table, and a composite-score chart. Its intended operational question is which represented airport profiles warrant closer review across passenger scale, route breadth, recovery and a score field.

The report is labelled UK/2022, but the project source map associates the displayed operational values with AVI0301-linked benchmark metrics; the archive has no source query/model export to resolve the field-level lineage.[2][3] The original remains unchanged in the gallery but is held from further release until source-to-field rights/lineage are resolved. GT1, GT8, GT9 and GT10 in the current V2 contracts provide conceptual analogues for market, connectivity, quality and scoped candidate outputs only; they do not verify this historical screen's metrics or score formula.

### 7. Operational monitoring filter — selected airport

![Original IBM Cognos selected-airport operational filter](historical-cognos-13-operational-filter-original.png)

This image shows a selected-Heathrow state of the operational page. The selector narrows KPI cards, route/recovery visuals, treemap, comparison table and composite-score view to the selected airport while retaining the comparison context. This is filter-state evidence, not an exported Cognos filter definition or a test of relationship direction/cardinality.

Source lineage remains unresolved in the project archive and the local map associates these displayed benchmark metrics with AVI0301-linked values.[2][3] No table row or metric value is repeated in this note. The original remains in the gallery but is held from further release pending source rights/lineage; it is not presented as a currently validated metric table.

### 8. Risk ranking — populated airport table and model fields

![Original IBM Cognos risk-ranking table](historical-cognos-14-risk-ranking-original.png)

The table exposes airport name, total passenger measure, route count, recovery-versus-2019 field, and a displayed composite-score field. This is the most operationally actionable historical view: it makes the candidate attributes inspectable rather than showing only a single KPI. The screenshot does not disclose the composite-score weights, normalisation population, missing-value policy, scenario, version, or audit trail; these must not be inferred from the column label.

The source archive does not establish the table's historical lineage. The local evidence map notes that the UK-labelled values may match AVI0301-linked metrics, but without source-to-field mapping this remains unresolved rather than a definitive source attribution.[2][3] The original is held from further release pending that mapping; its numeric rows are visible in the screenshot but are not repeated in prose. The current GT10 contract is candidate × decision scope × scenario × model version; it is not assumed to be the same as this historical Cognos score.

## Crosswalk to current code, SQL and validation

The current analytical implementation is separately inspectable in [`golden.py`](../../../../src/airtraffic/golden.py), [`scoring.py`](../../../../src/airtraffic/scoring.py), [`quality.py`](../../../../src/airtraffic/quality.py), [`sql/schema.sql`](../../../../sql/schema.sql), [`sql/views.sql`](../../../../sql/views.sql), and [`sql/validation_queries.sql`](../../../../sql/validation_queries.sql). Current GT1–GT10 grains, source lineage and scenario semantics are defined in [GT contracts](../../../gt-contracts.md), [lineage](../../../lineage.md), and the [decision model](../../../decision-model.md). Tests of current behaviour are in [`test_golden_tables.py`](../../../../tests/test_golden_tables.py), [`test_scoring.py`](../../../../tests/test_scoring.py), [`test_quality.py`](../../../../tests/test_quality.py), and [`test_pipeline.py`](../../../../tests/test_pipeline.py).

No original Cognos data module, package, SQL/query export, refresh log or report specification is included. Therefore the current code, SQL, local tests and public CI subset are evidence for the V2 implementation only; they do not validate the historical Cognos screenshots. All eight originals remain unchanged in the current gallery; the [per-image inventory](../../screenshot-release-inventory.md) distinguishes design candidates from held data-bearing images. The exact source ZIP and the [26-image index](../../README.md) are unchanged.

## Sources

[2] https://www.gov.uk/government/publications/aviation-statistics-notes-and-definitions/aviation-statistics-notes-and-definitions — DfT Aviation statistics: notes and definitions
[3] https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3 — Open Government Licence v3.0
[4] https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2022/may-2022 — CAA UK airport data May 2022
[12] https://www.caa.co.uk/Documents/Download/9070/47d4f858-9581-43d1-9ee5-9aebfaf3c83e/5062 — CAA Table 12.1 May 2022 PDF, Comparison with May 2021
