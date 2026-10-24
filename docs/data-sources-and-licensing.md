# Data sources, licensing and release inventory

## Scope and policy

`LICENSE` is the MIT license for original project code authored by Vladyslav Kononov; the owner has approved it. The MIT grant does **not** relicense third-party datasets, statistics, screenshots, dashboard content, model output, or other third-party materials. Their source terms continue to apply independently.

This audit separates publisher terms from the permission to include a particular derivative in Git. No license has been inferred from the fact that a dataset is aggregated, publicly viewable, or present in a local project folder. AVI0301/ICAO rights remain unresolved; related source files and derivatives stay local-only.

The project owner states they personally created the Power BI and IBM Cognos dashboard/report designs and analysis as academic work; Microsoft and IBM are the software platforms, not the dashboard authors. The owner also reports that the college supplied dataset links and learning resources. These statements establish project provenance/authorship context only; they do not grant rights to the vendor UI or third-party datasets.

## Sources

| Local source ID / file | Publisher and source URL | License / conditions observed | Release classification |
|---|---|---|---|
| `avi0105` — `data/raw/AVI0105.csv` | UK Department for Transport, [Aviation statistics tables](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-tables) and [AVI0105 notes](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-notes-and-definitions) | DfT aviation-statistics content is generally under Open Government Licence v3.0 unless an exception is stated. AVI0105 notes describe a CAA-return source and exclude data not cleared for release. Preserve DfT/source attribution and re-check the exact table notes when updating the input. | **B — attribution/conditions.** Raw input is not bundled; the local pipeline requires a privately obtained copy. |
| `avi0301` — `data/raw/AVI0301.csv` | DfT AVI0301, [aviation statistics tables](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-tables) and [notes](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-notes-and-definitions); DfT notes identify ICAO as the underlying source | The exact originating ICAO edition/URL is not recorded in the project, and the available DfT-wide OGL statement does not establish rights to republish ICAO-originated content or derivatives. No dataset-specific redistribution permission for this extract was verified. | **C — unresolved.** Raw input and all AVI0301-dependent outputs/screenshots are excluded from the public Git candidate pending rights confirmation. |
| `routes` — `data/raw/Table_12_1_Intl_Air_Pax_Traffic_Route_Analysis.csv` | UK Civil Aviation Authority, [Table 12.1, May 2022](https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2022/may-2022/) | CAA's published reuse notice requires the statistics to be referenced and prohibits selling/reselling the data. The GitHub portfolio candidate is intended to be free; retain explicit CAA attribution and do not sell/resell this data or its tables. | **B — attribution/conditions.** Selected route-derived outputs and screenshots may be included with attribution and the no-sale condition documented; raw input is not bundled. |
| `sfo` — `data/raw/Air_Traffic_Passenger_Statistics_2005-2020.csv` | San Francisco International Airport / DataSF, [Air Traffic Passenger Statistics, dataset `rkru-6vcg`](https://data.sf.gov/w/rkru-6vcg/ikek-yizv) | DataSF metadata identifies PDDL 1.0. Retain source provenance and confirm the archived snapshot corresponds to this dataset before redistributing it. | **B — provenance/conditions.** SFO-derived GT6 may be included with the dataset identified; raw input is not bundled. |

## Attribution text for any included data-bearing artifacts

Keep concise source credits alongside figures/tables and in the repository documentation:

- DfT: `Source: Department for Transport (DfT), aviation statistics table AVI0105. Licensed under the Open Government Licence v3.0 where no third-party exception applies.`
- CAA: `Source: UK Civil Aviation Authority (CAA), Table 12.1 International Air Passenger Traffic Route Analysis, May 2022.` CAA requires reference in publications and prohibits resale of its statistical data.
- SFO/DataSF: `Source: San Francisco International Airport / DataSF, Air Traffic Passenger Statistics (dataset rkru-6vcg; PDDL 1.0).`
- AVI0301: ICAO is identified as the source by DfT, but no attribution statement alone clears third-party redistribution rights. The data and dependent outputs remain excluded pending written/otherwise authoritative rights confirmation.

## GT1–GT10 output inventory

| Artifact | Source lineage | Class | Public-candidate treatment |
|---|---|---|---|
| GT1 — UK airport period totals | CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT2 — UK airport period change | GT1 / CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT3 — UK airport market ranking | GT1 / CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT4 — airport/destination-country flow | CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT5 — country traffic trends | DfT AVI0105 | B | Included with DfT attribution and AVI0105 table conditions. |
| GT6 — SFO historical benchmark | DataSF SFO dataset | B | Included with DataSF provenance/PDDL notice. |
| GT7 — global airport benchmark | DfT table containing ICAO-sourced data | C | Excluded: `outputs/golden/GT7_Global_Airport_Benchmark.csv`; source row values are not published. |
| GT8 — UK airport connectivity | CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT9 — operational KPI summary | Mixed: GT1/GT4/GT7/GT10 and source coverage | C | Excluded because it contains mixed-source KPI values, including GT7-derived counts and GT10 recommendation context. |
| GT10 — decision recommendations/scenarios | GT1/GT2/GT7/GT8 | C | The full mixed file is excluded because the global scope reproduces AVI0301-derived values; canonical results are not split or rewritten. |
| `docs/business-case-study.md` UK_SITE summary | UK-only GT2/GT8/CAA lineage | B | Publishes the UK_SITE baseline leader/stability as a short CAA-attributed narrative only; no GT10 row export, scores or global candidate values are included. |
| `outputs/golden_tables.xlsx` | GT1–GT10 | C | Excluded as a mixed workbook. The canonical workbook remains unchanged locally. |

`outputs/runs/` (including canonical run `20261005T163644Z_33f9f4ffa323`) remains intact locally and is ignored as a whole. It contains the canonical outputs and QA; it is not rewritten to evade the restrictions.

## QA, manifests and validation files

| Files | Class | Public-candidate treatment |
|---|---|---|
| `outputs/qa/gt10_eligibility_report.csv`, `gt10_sensitivity_summary.csv` | C | Excluded: contain candidate names/eligibility/ranks from AVI0301-linked global scoring. |
| `outputs/qa/quality_report.csv` | C | Excluded: contains source-level observed values and mixed GT10 checks; do not treat it as harmless merely because some rows are counts. |
| `outputs/qa/source_schema.txt` | C | Excluded: includes sample rows from AVI0301, not only column names. |
| `outputs/qa/run_metadata.json` | C | Excluded: includes per-table row counts for GT7/GT10; metadata copy with these counts remains local-only. |
| `outputs/qa/pipeline_run.txt`, `azure_validation.txt` | C | Excluded: recorded results include global candidate recommendations or detailed result rows. Azure transcript is historical, not freshly re-executed. |
| `outputs/qa/source_manifest.json`, `artifact_manifest.json` | A (metadata only) | Included as path/hash/size manifests only; they contain no source rows or metrics. Their hashes fingerprint local-only files and are not a substitute for permission to redistribute those files. |
| `docs/evidence/validation/release-validation-summary.md` | A (summary only) | Included; reports run status and quality-check outcome without table values, candidate names, source row counts or global scores. |

The code retains `EXPECTED_SOURCE_ROWS["avi0301"]` as input-version validation metadata only; it is a record-count check, not a passenger measure or airport row. The AVI0301-cleaning unit test now uses a synthetic example instead of copying a real airport name/traffic values. Detailed source cardinality/schema QA remains ignored locally.

## Screenshot and evidence inventory

| Evidence files | Source lineage/content | Class | Public-candidate treatment |
|---|---|---|---|
| Original CAA chart `docs/evidence/visualizations/uk-airport-market-snapshot.svg` | Independently authored graphic based only on permitted CAA GT3 output | B | Included with source/date credit and CAA no-sale condition; it is not a vendor screenshot and does not use AVI0301. |
| Original CAA chart `docs/evidence/visualizations/uk-site-demand-connectivity.svg` | Independently authored vendor-neutral figure from permitted GT1/GT4/GT8 CAA outputs | B | Included with CAA Table 12.1 May 2022 attribution and no-sale condition embedded in the figure; source-defined passenger periods, no vendor UI or AVI0301-derived result. |
| Original UK sensitivity summary `docs/evidence/visualizations/uk-site-scenario-stability.svg` | Original rendering of the already documented UK_SITE winner-only result using CAA-derived inputs; no score values or global rows | B | Included with CAA lineage notice; reports only the previously documented UK candidate stability, not a new score, global ranking, or forecast. |
| Original project timeline `docs/evidence/visualizations/project-evolution-timeline.svg` | Project-stage summary synthesized from repository documentation and local evidence; no third-party UI, source rows, or private identifiers | A (original project documentation visual) | Included; explicitly a chronological summary, not a vendor screenshot or technical migration claim. |
| Power BI `02-uk-market-demand`, `05b-scenario-sensitivity-uk`, `07b-candidate-detail-heathrow` | User-created report designs; CAA-derived UK metrics are B under CAA source terms; Microsoft UI appears in original capture | C (owner-authorized; residual vendor UI issue disclosed) | Included at the project owner's direction. CAA source reference/no-sale conditions are retained. This is not described as Microsoft permission or endorsement; these third-party-data screenshots do not qualify under Microsoft's default screenshot conditions. |
| Power BI `03-destination-connectivity` | User-created CAA-based report; map-source credits for OpenStreetMap, Microsoft, Esri Community Maps and Esri are visible | C (not cleared) | Local: attribution does not establish basemap reuse rights. Microsoft's standard screenshot permission has third-party-content and no-alteration conditions; a redacted derivative would not meet that standard. |
| Power BI `08-semantic-model-overview`, `09-relationships-overview` | User-created schema/relationship views; no source rows, third-party observations or identifiable person | A | Included unchanged and pixel-identical to originals with Microsoft’s required attribution; see screenshot guidance reference below. |
| Power BI `01-executive-decision-summary`, `04-global-expansion-benchmark`, `05a-scenario-sensitivity-global`, `06-data-quality-governance`, `07a-candidate-detail (global scope)` | Global candidate metrics/recommendations plus Microsoft UI | C | Excluded for AVI0301 content and third-party screenshot-content conditions. |
| IBM Cognos `07-semantic-model`, `11-demand-filter` | Owner-created model/UK demand report content; IBM Cognos UI; 07 shows schema metadata and 11 contains CAA-derived UK metrics | C (owner-authorized; residual vendor UI issue disclosed) | Included at the project owner's direction; no IBM permission or endorsement is claimed. CAA attribution/no-sale conditions apply to the UK data. |
| IBM Cognos `10-demand-recovery` | Owner-created UK-airport 2020-vs-2022 recovery report; IBM Cognos UI; source lineage for the historical series is not identified | C (not cleared) | Local until the original report/source documentation maps the multi-year measures to sources and establishes rights; the public CAA ROUTES snapshot cannot validate the historical series. Separate IBM UI screenshot terms are also needed. |
| IBM Cognos `08-executive-summary`, `09-executive-filter`, `12-operational-monitoring`, `13-operational-filter` | Owner-created report content; IBM UI; global benchmark values and operational values associated in the local source map with AVI0301 | C (not cleared) | Local-only until AVI0301 rights are confirmed and IBM screenshot/mark permission is documented. UK labels on some screens do not change the displayed source lineage. |
| IBM Cognos `14-risk-ranking` | Owner-created risk-ranking report with populated UK airport rows, passenger totals, route counts, recovery measures and composite-score fields; historical source lineage is not identified in the archive | C (not cleared) | Keep local until the source of the displayed measures and redistribution rights are established. The local evidence map flags AVI0301-matching values; do not infer that UK labels make the source CAA. |
| Azure `02-sql-resource-redacted` | Project Azure resource, personal/infrastructure identifiers in original; Microsoft Azure UI in screenshot | C (conditional) | Redacted capture is modified and the original exposes identifiers. Obtain a Microsoft exception for the altered image or replace it with an owner-created vendor-neutral diagram; keep the screenshot local meanwhile. |
| Azure `04-sql-validation-redacted` | User-run SQL validation work; Microsoft Azure UI | C (not cleared) | Result grid includes mixed GT10/global candidate rows. AVI0301 rights and screenshot permission are both unresolved. |
| Google Colab original `03-colab-azure-etl.png` and derivative `docs/evidence/historical/colab/colab-etl-upload-redacted.png` | Owner-authored historical notebook workflow; original includes mixed-source upload counts | C original (local); A derivative (published with output area masked) | The public derivative preserves the notebook code/connection workflow but fully masks upload-result lines containing AVI0301/GT7-derived counts; the untouched original remains in the archive/local. Google's [Brand Resource Center guidance](https://about.google/brand-resource-center/guidance/) permits Google brand elements solely for school projects. The image is presented only as the owner's academic project, does not show source result values, and does not imply Google endorsement or license aviation data. |
| IBM watsonx `05-import`, `06-autoai`, `10-autoai-experiment` | User-run import/experiment work; IBM watsonx UI; CAA metrics in AutoAI views | C (conditional) | User authorship of the workflow is acknowledged. Confirm applicable IBM screenshot/logo permission and whether the account-redacted copies may be published; CAA source attribution/no-sale conditions still apply. |
| SIPOC `historical-process-01-sipoc.png` | Diagram image; author/copyright metadata is not present in the archive | D | Preserve locally and exclude until the owner confirms authorship/publication rights; not covered by the code MIT license. |
| Unredacted Watsonx screenshots and `evidence-inbox/Data GitHub Project.zip` | Personal account/infrastructure UI and/or unreviewed originals | D | Local-only and ignored; never included in public candidate. |

The original ZIP, the original screenshots and every canonical run artifact are preserved locally. Redacted Watsonx publication copies are separate files; originals are not overwritten. No synthetic or replacement aviation data was created.

The two included Microsoft Power BI model screenshots were checked pixel-for-pixel against the original copies and contain no third-party data rows or identifiable person. Microsoft’s [published screenshot guidance](https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions) permits product screenshots in websites/documentation only when its conditions are met, including no third-party content or identifiable people, no alteration beyond resizing, full product naming, and the statement “Used with permission from Microsoft.” Microsoft explicitly says it cannot grant permission for third-party content. That attribution is retained only for the two data-free schema captures and does not imply endorsement or bespoke consent.

Three CAA-bearing Power BI report screenshots and two Cognos captures are included at the project owner's direction. The Cognos set includes the CAA-derived demand filter; the schema capture has no source rows. These authentic user-authored works are **not** represented as Microsoft or IBM permission; the residual product-UI/branding issue remains disclosed. CAA attribution and the no-sale condition are retained where applicable. IBM's published [copyright/trademark guidance](https://www.ibm.com/legal/copyright-trademark) addresses express written permission for IBM logo use and limits fair-use trademark references to text; it does not itself establish permission for each Cognos UI screenshot. Google's [Brand Resource Center guidance](https://about.google/brand-resource-center/guidance/) permits Google brand elements solely for school projects; the public Colab derivative is limited to that academic-project context and masks all result values, while its original remains local. This does not grant rights to AVI0301-derived data or imply endorsement. The redacted Azure capture also remains local because it is altered Microsoft UI and the original exposes infrastructure identifiers. These distinctions do not assert a universal prohibition where the applicable terms or legal basis are unresolved.

## Code license boundary

The root `LICENSE` is the owner-approved MIT license for original project code only. Third-party data, statistical content, screenshots, dashboard captures, and other publisher materials are outside that grant and remain subject to their own terms.
