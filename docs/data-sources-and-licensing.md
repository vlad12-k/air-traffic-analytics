# Data sources, licensing and release inventory

## Scope and policy

`LICENSE` is retained as MIT for original owner-authored software only. It does **not** relicense third-party datasets, statistics, screenshots, dashboard content, model output, or other third-party materials. Their source terms continue to apply independently; authorship of a derived result does not itself settle the rights in its inputs.

This inventory separates owner-authored software and screenshot composition from third-party data, map layers, platform UI and source terms. Owner authorship or a direction to preserve an image does not license embedded statistics or account/infrastructure metadata. The local archive contains 26 original PNGs; 25 exact originals are linked in the working-tree galleries, with Dubai 07a local/untracked. The public GitHub `main` branch already exposes historical screenshots, including some with global AVI0301-associated values and Azure account/resource context. The [per-image screenshot inventory](evidence/screenshot-release-inventory.md) records content and review basis; five selected screenshots received owner full-resolution visual review, while other originals are described from OCR and existing technical notes. Visual review is not rights clearance. No image, source file, or canonical output is altered by this documentation work.

## Local source inventory

The source manifest records the local path, byte size and SHA-256 for four privately obtained inputs; it does not record download timestamps or a historical URL for each snapshot. Pipeline configuration records file paths, not source editions. The original Unit 19 periods below are the periods stated by the owner; the brief itself is not copied into this repository. Exact official publishers, current public links and rights caveats appear in [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

| Local source ID / file | Publisher and source URL | License / conditions observed | Release classification |
|---|---|---|---|
| `avi0105` — `data/raw/AVI0105.csv` | Department for Transport (DfT), [AVI tables landing page](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-data-tables-avi), [AVI0105 ODS](https://assets.publishing.service.gov.uk/media/6936e31a92da4705a575d42b/avi0105.ods), and [aviation notes](https://www.gov.uk/government/publications/aviation-statistics-notes-and-definitions/aviation-statistics-notes-and-definitions) | Local snapshot is 2013–2023; current official ODS is 2014–2024.[1][2][9] DfT identifies CAA data lineage; OGL v3.0 does not license third-party rights DfT is not authorised to grant.[2][3] | **B — conditional on DfT/CAA terms and attribution.** GT5 reproduces every local category/year cell after a unit conversion; see the [tracked-table analysis](../outputs/golden/README.md). |
| `avi0301` — `data/raw/AVI0301.csv` | DfT, [AVI tables landing page](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-data-tables-avi), [AVI0301 ODS](https://assets.publishing.service.gov.uk/media/6936e3a76a167b6884b73640/avi0301.ods), and [aviation notes](https://www.gov.uk/government/publications/aviation-statistics-notes-and-definitions/aviation-statistics-notes-and-definitions) | DfT identifies ICAO as the underlying source.[2] The exact source edition, local download URL and ICAO redistribution permission are not recorded; OGL's third-party exception remains relevant.[3] Current DfT file is 2023-era, not the local 2021–2022 table.[10][11] | **C — rights unresolved.** Keep raw data and AVI0301-derived global values/screenshots out of any new release until authoritative permission is documented; do not call ICAO data open-licensed. |
| `routes` — `data/raw/Table_12_1_Intl_Air_Pax_Traffic_Route_Analysis.csv` | UK Civil Aviation Authority, [Table 12.1 May 2022 source page](https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2022/may-2022/) and [Table 12.1 PDF](https://www.caa.co.uk/Documents/Download/9070/47d4f858-9581-43d1-9ee5-9aebfaf3c83e/5062) | The local input has 1,752 route rows and `this_period=202205`; the official Table 12.1 comparison is May 2022 vs May 2021.[12] CAA requires reference/attribution and says its statistics may not be sold on to a third party; do not characterize this as unrestricted OGL.[4] | **B — attribution/no-sale conditions.** Free portfolio display with explicit CAA source credit is the proposed treatment; do not sell/resell the source statistics or claim MIT rights over them. |
| `sfo` — `data/raw/Air_Traffic_Passenger_Statistics_2005-2020.csv` | San Francisco International Airport / DataSF, [Air Traffic Passenger Statistics dataset `rkru-6vcg`](https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg) and [dataset details](https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg/about_data) | DataSF metadata identifies PDDL 1.0.[6][14] Local snapshot has 31,339 rows and activity periods 2005-01 through 2025-07, despite the stale 2005-2020 filename. DataSF describes airline-reported monthly data.[5] | **B — PDDL/provenance.** GT6 is a 21-row annual aggregate; the raw input is not tracked or bundled. |

## Source-version reconciliation

| Source | Owner-provided Unit 19 period / statement | Observed local snapshot and pipeline evidence | Current official publication | Documentation-only disposition |
|---|---|---|---|---|
| AVI0105 | Assignment brief: 2011–2021. | Local `AVI0105.csv`: 77 source categories, year columns 2013–2023. `clean.py` selects 2013–2023; `config.py` points at this CSV. Manifest stores hash/size but no download date or URL. | Current DfT ODS covers 2014–2024.[1][2][9] | State all three windows separately. Do not silently replace local values or call the current live table the original assignment snapshot. |
| AVI0301 | Assignment brief: 2019–2020. | Local file has 25 rows with 2021/2022 passenger and movement columns; V2 contracts/documentation describe 2021–2022. Config and manifest identify only the file path/hash, not source release/permission. | Current DfT AVI0301 ODS is a 2023-era publication; ICAO separately publishes 2023 statistical results.[10][11] | Describe the local table as 2021–2022 and distinguish it from the assignment window and current edition. The raw input and GT7/GT9/GT10 CSV outputs are not in tracked golden tables, but some existing public screenshots display global/mixed results; permission remains unresolved and no new clearance is claimed. |
| SFO / DataSF | Assignment context uses the SFO passenger benchmark. | Filename is `Air_Traffic_Passenger_Statistics_2005-2020.csv`; actual local `Activity Period` range is 200501–202507 (31,339 rows). GT6 has 21 annual rows, 2005–2025. | DataSF dataset page identifies the current dataset and PDDL metadata.[5][6][14] | Keep the source filename as-is, but document the observed 2005–2025 local coverage and stale filename. No source file was renamed or changed. |
| CAA Table 12.1 | Prior public README text and historical Cognos screenshots used a 2020 comparison label. | Local route file has `this_period=202205`; prior passenger values are in `total_pax_last_period` (no separate prior-period code is stored in that CSV). | Official Table 12.1 PDF identifies May 2022 compared with May 2021.[12] | Correct narrative to “May 2022 vs May 2021”; preserve original fields, analytical values and screenshot pixels. Captions must identify the archived 2020 label as a historical discrepancy, not as the official source period. |

The owner-provided assignment brief is the source for the assignment-period statements above; its exact page is not copied into the repository, so those assignment periods are not an independently extractable project artifact. The local config/manifests do not establish when the files were obtained. These are documentation/provenance corrections only; no input, output, calculation, source hash, or pipeline configuration was modified.

## Attribution text for any included data-bearing artifacts

Keep concise source credits alongside figures/tables and in the repository documentation:

- DfT AVI0105: `Source: Department for Transport (DfT), AVI0105 (TSGB0205), International passenger movements at UK airports by last or next country travelled to; underlying source identified by DfT as CAA.` Apply OGL v3.0 only where the provider has authority and no third-party exception applies.[2][3][9]
- CAA: `Source: UK Civil Aviation Authority (CAA), Table 12.1 International Air Passenger Traffic Route Analysis, May 2022; comparison with May 2021.` CAA requires reference in publications and prohibits resale of its statistical data.[4][12]
- SFO/DataSF: `Source: San Francisco International Airport / DataSF, Air Traffic Passenger Statistics (dataset rkru-6vcg; PDDL 1.0).`[5][14]
- AVI0301: ICAO is identified as the source by DfT, but no attribution statement alone clears third-party redistribution rights. The data and dependent outputs remain excluded pending written/otherwise authoritative rights confirmation.

## GT1–GT10 output inventory

| Artifact | Source lineage | Class | Public-candidate treatment |
|---|---|---|---|
| GT1 — UK airport period totals | CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT2 — UK airport period change | GT1 / CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT3 — UK airport market ranking | GT1 / CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT4 — airport/destination-country flow | CAA `ROUTES`; 666 rows cover every airport-country pair from 1,752 input route rows | B | Complete country-level aggregation; substantial derived reproduction, not raw row copying. CAA attribution/no-sale condition; MIT does not apply to the statistics. |
| GT5 — country traffic trends | DfT AVI0105; all 77 × 11 = 847 local source cells | B | Full transformed table after unit scaling, plus derived growth/index fields; DfT/CAA source terms apply. |
| GT6 — SFO historical benchmark | DataSF SFO; all 31,339 local input rows, aggregated to 21 annual rows | B | Derived annual aggregate; retain dataset provenance/PDDL notice. |
| GT7 — global airport benchmark | DfT table containing ICAO-sourced data | C | No GT7 CSV is in tracked `outputs/golden/`. Existing public screenshots do show AVI0301-associated global names/values/ranks; their rights remain unresolved. Preserve the original screenshots and do not represent attribution alone as permission. |
| GT8 — UK airport connectivity | CAA `ROUTES` | B | Included with CAA attribution and no-sale condition. |
| GT9 — operational KPI summary | Mixed: GT1/GT4/GT7/GT10 and source coverage | C | No GT9 CSV is in tracked `outputs/golden/`. Some existing screenshots expose coverage or stability values associated with global inputs; rights and historic field lineage remain unresolved. |
| GT10 — decision recommendations/scenarios | GT1/GT2/GT7/GT8 | C | No GT10 CSV is in tracked `outputs/golden/`. Existing screenshots include mixed/global recommendations and scores; the exact local AVI0301 source edition and redistribution permission are unresolved. Owner authorship/preservation instruction does not license source data. |
| `docs/business-case-study.md` UK_SITE summary | UK-only GT2/GT8/CAA lineage | B | Publishes the UK_SITE baseline leader/stability as a short CAA-attributed narrative only; no GT10 row export, scores or global candidate values are included. |
| `outputs/golden_tables.xlsx` | GT1–GT10 | C | Excluded as a mixed workbook. The canonical workbook remains unchanged locally. |

The exact per-file tracked CSV inventory, field lists, record counts, comparisons and full-versus-derived findings are in [`outputs/golden/README.md`](../outputs/golden/README.md). `A` means metadata/non-data; `B` means source-derived content with stated conditions; `C` means rights or lineage unresolved. These categories describe evidence status, not repository visibility, a removal instruction, or a licence.

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

The 26-image [per-image evidence inventory](evidence/screenshot-release-inventory.md) records exact repository paths, original/derivative status, stage, OCR-visible content, source periods, limitations and identified privacy/rights questions. It distinguishes data-bearing CAA/ICAO/map content from model/process evidence and account/infrastructure metadata. A vendor interface alone is not a reason to prohibit an image; the inventory describes item-specific issues and does not grant permission.

The source ZIP and all 26 original PNGs remain unchanged; the archive-matched copies were SHA-256 checked. No redaction, replacement, relocation or deletion was made. Five selected screenshots had owner full-resolution visual review in the earlier evidence assessment; the remaining archive images have OCR-level descriptions and are not represented as fully visually reviewed. The originals and links are preserved as instructed. The public `main` branch already contains image files with visible Azure account/resource context and images displaying AVI0301-associated results; these are material privacy/rights questions to raise with the owner, not a basis for claiming all vendor screenshots are prohibited. Documentation alone does not resolve them, and no remote change or publication was made here.

## Code license boundary

The root `LICENSE` remains MIT for original owner-authored software only. Third-party data, statistics, screenshots, dashboard captures, maps and publisher materials are outside that grant and remain subject to their own terms.

## Sources

[1] https://www.gov.uk/government/statistical-data-sets/aviation-statistics-data-tables-avi — DfT Aviation statistics: data tables (AVI)
[2] https://www.gov.uk/government/publications/aviation-statistics-notes-and-definitions/aviation-statistics-notes-and-definitions — DfT Aviation statistics: notes and definitions
[3] https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3 — Open Government Licence v3.0
[4] https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2022/may-2022 — CAA UK airport data May 2022
[5] https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg/about_data — DataSF Air Traffic Passenger Statistics
[6] https://opendatacommons.org/licenses/pddl/1-0 — Open Data Commons PDDL v1.0
[9] https://assets.publishing.service.gov.uk/media/6936e31a92da4705a575d42b/avi0105.ods — DfT AVI0105 ODS, updated 17 December 2025
[10] https://assets.publishing.service.gov.uk/media/6936e3a76a167b6884b73640/avi0301.ods — DfT AVI0301 ODS, updated 17 December 2025
[11] https://www.icao.int/presentation-2023-air-transport-statistical-results — ICAO 2023 Air Transport Statistical Results
[12] https://www.caa.co.uk/Documents/Download/9070/47d4f858-9581-43d1-9ee5-9aebfaf3c83e/5062 — CAA Table 12.1 May 2022 PDF, Comparison with May 2021
[14] https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg — DataSF Air Traffic Passenger Statistics dataset
