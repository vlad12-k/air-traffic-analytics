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
| Power BI `02-uk-market-demand`, `03-destination-connectivity`, `05b-scenario-sensitivity-uk`, `07b-candidate-detail-heathrow` | User-created report designs; CAA/DfT data is B under its source terms; Microsoft UI appears in capture | C (conditional) | Not currently included. Standard Microsoft guidance excludes third-party content; an applicable written exception/permission or a rights-cleared vendor-neutral export would resolve the screenshot issue, in addition to source attribution. This is a conditional status, not a claim that every use is prohibited. |
| Power BI `08-semantic-model-overview`, `09-relationships-overview` | User-created schema/relationship views; no source rows, third-party observations or identifiable person | A | Included unchanged and pixel-identical to originals with Microsoft’s required attribution; see screenshot guidance reference below. |
| Power BI `01-executive-decision-summary`, `04-global-expansion-benchmark`, `05a-scenario-sensitivity-global`, `06-data-quality-governance`, `07a-candidate-detail (global scope)` | Global candidate metrics/recommendations plus Microsoft UI | C | Excluded for AVI0301 content and third-party screenshot-content conditions. |
| IBM Cognos `07-semantic-model`, `10-demand-recovery`, `11-demand-filter` | Owner-created model/report content; IBM Cognos UI; no AVI0301 values observed in these captures | C (conditional) | Not currently included. Confirm applicable IBM screenshot/UI terms or obtain permission for the capture (including any IBM logos/marks); CAA attribution/no-sale still applies to route metrics. Missing evidence is not a conclusion that all reuse is prohibited. |
| IBM Cognos `08-executive-summary`, `09-executive-filter`, `12-operational-monitoring`, `13-operational-filter`, `14-risk-ranking` | Owner-created report content; IBM UI; several images show AVI0301-matching global benchmark values | C (not cleared) | Local-only until AVI0301 rights are confirmed and IBM screenshot/mark permission is documented. UK labels on some screens do not change the displayed source lineage. |
| Azure `02-sql-resource-redacted` | Project Azure resource, personal/infrastructure identifiers in original; Microsoft Azure UI in screenshot | C (conditional) | Redacted capture is modified and the original exposes identifiers. Obtain a Microsoft exception for the altered image or replace it with an owner-created vendor-neutral diagram; keep the screenshot local meanwhile. |
| Azure `04-sql-validation-redacted` | User-run SQL validation work; Microsoft Azure UI | C (not cleared) | Result grid includes mixed GT10/global candidate rows. AVI0301 rights and screenshot permission are both unresolved. |
| Google Colab `03-azure-etl-redacted` | User-run notebook ETL/upload workflow; Google Colab UI | C (not cleared) | Upload log includes AVI0301/GT7 output counts; rights for the values and screenshot reuse terms must both be confirmed. |
| IBM watsonx `05-import`, `06-autoai`, `10-autoai-experiment` | User-run import/experiment work; IBM watsonx UI; CAA metrics in AutoAI views | C (conditional) | User authorship of the workflow is acknowledged. Confirm applicable IBM screenshot/logo permission and whether the account-redacted copies may be published; CAA source attribution/no-sale conditions still apply. |
| SIPOC `historical-process-01-sipoc.png` | Diagram image; author/copyright metadata is not present in the archive | D | Preserve locally and exclude until the owner confirms authorship/publication rights; not covered by the code MIT license. |
| Unredacted Watsonx screenshots and `evidence-inbox/Data GitHub Project.zip` | Personal account/infrastructure UI and/or unreviewed originals | D | Local-only and ignored; never included in public candidate. |

The original ZIP, the original screenshots and every canonical run artifact are preserved locally. Redacted Watsonx publication copies are separate files; originals are not overwritten. No synthetic or replacement aviation data was created.

The two included Microsoft Power BI model screenshots were checked pixel-for-pixel against the original copies and contain no third-party data rows or identifiable person. Microsoft’s screenshot guidance permits product screenshots only when its conditions are met, including no third-party content, no alterations beyond resizing, full product naming and the statement “Used with permission from Microsoft.” The public README/evidence index carries that product name and statement. Data-bearing Power BI pages and the redacted Azure capture are excluded rather than assuming they qualify. IBM’s published [copyright/trademark guidance](https://www.ibm.com/legal/copyright-trademark) says IBM logo use requires express written permission and trademark fair use is limited to text references; this does not itself resolve reuse of Cognos/watsonx UI captures. Confirm applicable product terms or obtain written IBM screenshot permission. Google’s [general Terms of Service](https://policies.google.com/terms) are recorded for Colab; no product-specific screenshot reuse grant was found in the project evidence, so obtain applicable permission/terms before publishing Colab UI captures. These conditional statuses are not blanket findings that all reuse is prohibited.

## Code license boundary

The root `LICENSE` is the owner-approved MIT license for original project code only. Third-party data, statistical content, screenshots, dashboard captures, and other publisher materials are outside that grant and remain subject to their own terms.
