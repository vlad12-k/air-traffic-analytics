# Data sources, licensing and release inventory

## Scope and policy

`LICENSE` is the MIT license for original project code authored by Vladyslav Kononov; the owner has approved it. The MIT grant does **not** relicense third-party datasets, statistics, screenshots, dashboard content, model output, or other third-party materials. Their source terms continue to apply independently.

This inventory distinguishes the owner’s authorization to publish their authored screenshots from source-data conditions and vendor endorsement. The owner authorizes their screenshot work; that permission does not independently clear third-party data, map or platform conditions. The source archive has 26 originals; 25 are in the public galleries. The Dubai 07a Power BI image remains local-only because AVI0301/ICAO data rights and screenshot conditions are unresolved. Raw CSVs and canonical row-level output files remain excluded; applicable source attribution/no-resale notices are retained.

## Sources

The owner confirms authorship of all 26 archive images and authorizes publication of their screenshot work. That authorisation is the basis for publishing the 25 cleared originals in this release; it does not imply vendor endorsement or independently clear third-party source data or screenshot conditions. The Dubai 07a Power BI original remains local-only pending those clearances. No raw source CSVs are bundled. CAA attribution/no-sale conditions and other source provenance are still disclosed. The owner reports the college supplied source links and learning resources.

| Local source ID / file | Publisher and source URL | License / conditions observed | Release classification |
|---|---|---|---|
| `avi0105` — `data/raw/AVI0105.csv` | UK Department for Transport, [Aviation statistics tables](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-tables) and [AVI0105 notes](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-notes-and-definitions) | DfT aviation-statistics content is generally under Open Government Licence v3.0 unless an exception is stated. AVI0105 notes describe a CAA-return source and exclude data not cleared for release. Preserve DfT/source attribution and re-check the exact table notes when updating the input. | **B — attribution/conditions.** Raw input is not bundled; the local pipeline requires a privately obtained copy. |
| `avi0301` — `data/raw/AVI0301.csv` | DfT AVI0301, [aviation statistics tables](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-tables) and [notes](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-notes-and-definitions); DfT notes identify ICAO as the underlying source | The exact originating ICAO edition/URL is not recorded in the project. The owner expressly authorizes publication of the original authored screenshots containing historical derived values; that does not grant access to or distribute the raw CSV. | **C — raw input excluded.** Historical screenshot evidence is included based on owner authorization and identified as archival, not as current/revalidated output. |
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
| GT7 — global airport benchmark | DfT table containing ICAO-sourced data | C | Raw output `outputs/golden/GT7_Global_Airport_Benchmark.csv` remains excluded; historical values may be visible within the authorized original screenshots. |
| GT8 — UK airport connectivity | CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT9 — operational KPI summary | Mixed: GT1/GT4/GT7/GT10 and source coverage | C | Raw mixed-source KPI outputs are excluded; historical dashboard screenshots are included with their displayed values identified as archival. |
| GT10 — decision recommendations/scenarios | GT1/GT2/GT7/GT8 | C | Canonical mixed output files remain excluded; selected historical dashboard screenshots may display archival results under the owner's authorization. |
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
| Power BI `01`–`09` report/model screenshots (11 archive entries) | User-created report designs; CAA measures, AVI0301-associated historical values, map-source credits and Power BI UI appear as applicable | C (owner-authorized original screenshots) | Ten exact archive originals are published; the Dubai 07a capture remains local-only because AVI0301/ICAO source rights and screenshot conditions are unresolved. CAA attribution/no-sale conditions and visible map credits are retained where relevant. |
| IBM Cognos `07`–`14` screenshots (eight archive entries) | User-created report/model work; IBM Cognos UI and historical CAA/AVI0301-associated measures appear as applicable | C (owner-authorized original screenshots) | All eight exact archive PNGs included under the owner's express publication authorization. CAA attribution/no-sale conditions remain applicable where relevant; no IBM endorsement is claimed. |
| Azure `02-sql-resource` | Historical Azure resource/database view; resource/account context and Microsoft Azure UI are visible | C (owner-authorized original screenshot) | Exact archive original included at the owner's direction. It is historical UI evidence only; no live resource was accessed or changed. |
| Azure `04-sql-validation` | Historical query/result view; mixed GT10/global candidate fields and Azure UI | C (owner-authorized original screenshot) | Exact archive original included at the owner's direction. It does not establish independent reconciliation or a current run; no raw CSV is bundled. |
| Google Colab original `03-colab-azure-etl.png` and redacted derivative | Owner-authored historical notebook workflow; original includes upload output | C (owner-authorized original) / A (separate derivative) | Both the exact original and a separately labeled authentic redacted derivative are included. The derivative masks the complete output block and does not replace the original. No raw CSV is included or Google endorsement claimed. |
| IBM watsonx `05-import`, `06-autoai`, `10-autoai-experiment` | User-created import/experiment work; IBM UI, account context and historical evaluation metrics are visible | C (owner-authorized original screenshots) | All three exact archive PNGs included. No model export, reproducible training artifact, independent holdout evaluation or IBM endorsement is claimed. |
| SIPOC `historical-process-01-sipoc.png` | Owner-authored process diagram; authorship/publication expressly confirmed by the owner | A | Included as the exact archive PNG; publication relies on owner permission for the original diagram, not the code MIT license. |
| `evidence-inbox/Data GitHub Project.zip` | Original source archive containing all 26 PNGs | D | Kept unchanged as the local source-of-truth archive; the selected exact PNGs are separately copied into their public evidence galleries. |

The original ZIP and every canonical run artifact are preserved unchanged locally. Twenty-five exact archive-original PNGs are copied into the public evidence galleries; the Dubai 07a original remains local pending source-rights and screenshot-condition clearance. The Colab redacted derivative and duplicate review/model-view files are distinct assets and do not replace or increase the original count. No synthetic or replacement aviation data was created.

The 25 published originals were checked against the ZIP by SHA-256. The withheld Dubai 07a archive entry was also byte-verified locally but not published. The owner's authorization covers the authored screenshot work as represented by the owner; it does not clear third-party rights or imply vendor endorsement or live product use. Visible third-party source credits and CAA attribution/no-sale conditions are retained on published images where relevant. Raw CSV inputs, credentials and canonical row-level output files remain excluded.

IBM, Microsoft, Azure, Google Colab and watsonx product interfaces are shown only as part of owner-authored historical project evidence. No claim of vendor sponsorship, endorsement, certification, or bespoke product permission is made. Source-data and map credits remain separately identified; the code MIT license does not override them.

## Code license boundary

The root `LICENSE` is the owner-approved MIT license for original project code only. Third-party data, statistical content, screenshots, dashboard captures, and other publisher materials are outside that grant and remain subject to their own terms.
