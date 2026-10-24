# Historical IBM Cognos — technical walkthrough of published original screenshots

These two original PNGs are the currently published Cognos captures. The project owner states they authored the report and model; IBM Cognos was the reporting platform. No IBM permission, endorsement, current deployment, refresh, or export package is claimed. The UK demand filter contains CAA-derived data and retains the attribution/no-resale conditions stated in the project source record.

The sequence follows the historical workflow: inspect the semantic model → use a UK airport selection to review reported demand.

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

**What the screenshot evidences.** The visible report is titled “UK decision pack (Top 10 UK airports, 2022)” and shows an airport list/filter with Heathrow selected. It includes total passengers, average monthly passengers, a top-airport ranking, and period-comparison/growth views. The capture visibly reports 4,993,568 for Heathrow in 2022, 567,162 in 2020, and a recovery multiple of 7.8; several other values/labels are small or OCR-ambiguous and are intentionally not transcribed here.

**Model and filters.** The report is an interactive Cognos page with a UK airport selection and a top-10 presentation. The project source inventory associates this historical UK view with CAA-derived route measures, but the screenshot itself labels a 2020-versus-2022 comparison. The present V2 CAA ROUTES contract is a comparison snapshot (period 202205), not a multi-year UK airport series. The exact historical field-to-source mapping and transformation behind the 2020/2022 values are therefore not reproducible from the public project files; do not equate the capture's period comparison with GT2 without that lineage.

**Interpretation and decision.** The page communicates Heathrow's leading displayed 2022 passenger total and a substantial historical recovery multiple, supporting further investigation of Heathrow in the historical decision pack. Recovery in airport passenger totals is not retail footfall, and the ratio is not a sales forecast.

**Validation and limitations.** No historical Cognos query, source-row extract, or independent recalculation is included, so displayed values are screenshot evidence rather than a revalidated result. The current V2 pipeline's recorded quality run does not validate this historical report. CAA Table 12.1, May 2022, attribution/no-resale conditions are retained per the project source record, but the screenshot's 2020/2022 lineage discrepancy remains explicit. IBM UI is visible; no IBM permission or endorsement is claimed.

## Other original Cognos archive pages not published

Six other Cognos PNGs remain local for the specific reasons recorded in the [complete evidence inventory](../../README.md):

- `08-cognos-executive-summary.png` and `09-cognos-executive-filter.png` — global comparisons use AVI0301/ICAO values with unresolved redistribution rights.
- `10-cognos-demand-recovery.png` — the screenshot is a UK airport 2020-vs-2022 recovery view, but its underlying source lineage is not identified; the public CAA ROUTES contract is a comparison snapshot and does not substantiate this historical series.
- `12-cognos-operational-monitoring.png` and `13-cognos-operational-filter.png` — populated operational views include airport metrics associated in the local evidence map with AVI0301-matching benchmark values; data rights remain unresolved.
- `14-cognos-risk-ranking.png` — the original contains populated UK airport rows and passenger, route, recovery, and composite-score fields. Its historical source lineage is not established in the archive; do not publish those values until the source and redistribution rights are mapped.

No report was recreated or redacted. The owner's authorship authorization does not clear third-party data rights. The preserved original `14-cognos-risk-ranking.png` remains local and is not included in the public gallery.