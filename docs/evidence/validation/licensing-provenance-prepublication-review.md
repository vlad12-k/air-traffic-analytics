# Licensing, provenance and pre-publication review

**Status: Documentation review for this PR; this document does not grant screenshot, dataset, map or vendor-interface publication permission.** It records a documentation-only review. Owner approval of this documentation PR is not approval to alter or further publish evidence assets; unresolved rights and privacy issues remain open.

## Scope and verification basis

The owner-provided Unit 19 brief supplies the assignment periods; the brief itself is not stored as a repository artifact. Local findings below were checked against `outputs/qa/source_manifest.json`, `src/airtraffic/config.py`, the ingestion/cleaning code, tracked CSV inventory, local source files and outputs, the screenshot archive, and the current CI workflow. All four locally available input files matched their manifest SHA-256 and byte-size entries. Period/version differences are described, not repaired by changing data or configuration.

The audit found only seven tracked CSVs, all under `outputs/golden/`: GT1, GT2, GT3, GT4, GT5, GT6 and GT8. No source CSV, original AVI0301 CSV, GT7/GT9/GT10 CSV output, or complete source dataset is tracked. The two tracked source/artifact manifests contain path, hash and size metadata only. The local source rows and canonical outputs were read-only inputs to validation.

## Dataset inventory and reproduction assessment

| Tracked artifact | Actual rows and fields | Lineage and coverage | Full versus derived assessment |
|---|---|---|---|
| `GT1_UK_Airport_Period_Totals.csv` | 36 rows; `run_id`, `airport_name`, `passengers_current`, `passengers_prior`, `absolute_change`, `comparison_period` | CAA Table 12.1 route snapshot, `this_period=202205`; prior passenger values are in `total_pax_last_period`. | Airport-level aggregation for all 36 airports represented in this snapshot; not the 1,752 route records and not a multi-year series. |
| `GT2_UK_Airport_Period_Change.csv` | 36 rows; GT1 fields plus `growth_pct`, `zero_baseline` | Derived from GT1 / CAA route snapshot. | Reuses the complete represented airport-total population and adds calculated change/denominator flags; no new source rows. |
| `GT3_UK_Airport_Market_Ranking.csv` | 36 rows; `run_id`, `rank`, `airport_name`, `comparison_period`, `passengers_current`, `passengers_prior`, `absolute_change`, `market_share_pct` | Derived from GT1 / CAA route snapshot. | Ranks and calculates share over all 36 represented airports; it does not reproduce route-level records or the complete source table. |
| `GT4_Airport_Destination_Country_Flow.csv` | 666 rows; `run_id`, `airport_name`, `destination_country`, `passengers_current`, `destination_airport_count`, `airport_flow_share_pct`, `rank_within_airport` | CAA route snapshot: 1,752 input rows. | Contains all 666 unique airport × destination-country pairs from the local input. Pair coverage and passenger sums reconciled with zero missing/extra pairs or mismatches. This is not a raw row copy, but it is a complete, substantial aggregation of the source's observed pair domain. |
| `GT5_Country_Traffic_Trends.csv` | 847 rows; `run_id`, `region`, `country`, `year`, `passengers`, `pct_of_total_2023`, `annual_growth_pct`, `passengers_2019`, `index_vs_2019` | Local AVI0105: 77 categories × 11 years (2013–2023). | All 847 category/year passenger cells match after converting source thousands to passenger counts. Growth/index fields are derived; all compared values, including those fields, reconciled at `rtol=1e-9`, `atol=1e-9` (zero mismatches). This is a full transformed reproduction of the local table, not a sample. |
| `GT6_SFO_Historical_Benchmark.csv` | 21 rows; `run_id`, `year`, `domestic_passengers`, `international_passengers`, `total_passengers`, `classified_passengers`, `classification_delta`, `international_share_pct`, `annual_growth_pct` | All 31,339 rows in the local SFO input; activity periods 2005-01 through 2025-07. | Annual domestic/international aggregation for 2005–2025, not raw row republication. All annual totals and derived values reconciled at the stated floating-point tolerance. |
| `GT8_UK_Airport_Connectivity.csv` | 36 rows; `run_id`, `airport_name`, `passengers_current`, `destination_country_count`, `destination_airport_count`, `scheduled_passengers`, `charter_passengers`, `scheduled_share_pct`, `charter_share_pct`, `component_reconciliation_delta` | Derived from CAA route records for the same represented UK-airport population. | Airport-level connectivity and traffic-mix summaries, not raw route rows. It summarizes the full represented population but does not reproduce every route record. |

GT1, GT2, GT3, GT4, GT5, GT6 and GT8 were independently reconstructed from local inputs using the project ingestion/cleaning/transform functions and compared with the tracked CSVs. Every expected key/row matched; all checked values had zero mismatches at `rtol=1e-9`, `atol=1e-9`. Small differences in calculated percentages/growth are only floating-point representation at machine precision. The full actual field lists are in [`outputs/golden/README.md`](../../../outputs/golden/README.md). The calculations and CSVs were not changed.

## Source-version reconciliation

| Source | Assignment brief | Local configuration/manifest and source file | Current official publication evidence | Documentation-only conclusion |
|---|---|---|---|---|
| AVI0105 | 2011–2021 | Local file has 77 categories and columns 2013–2023; `clean.py` selects that local span. Manifest records path/hash/size, not acquisition date or original URL. | DfT's current AVI0105 ODS title covers 2014–2024; DfT identifies the underlying series as CAA data.[2][9] | Keep assignment, local snapshot, and current ODS windows distinct. Do not replace any source/output values or imply that the current ODS is the historical input. The exact rights basis for this historical CAA-derived local table remains to be confirmed. |
| AVI0301 | 2019–2020 | Local file has 25 rows and 2021/2022 passenger and movement columns; current config/manifest identify only the file path/hash. Existing V2 documentation uses 2021–2022. | DfT's current ODS is a 2023 global-airport edition; DfT notes say AVI0301 is based on ICAO data. ICAO separately presents 2023 statistical results.[2][10][11] | Describe the local file as 2021–2022, separate it from both the assignment period and the current DfT edition, and keep global data-bearing outputs/screenshots held. No source edition or redistribution permission has been established. |
| SFO / DataSF | SFO passenger benchmark in the assignment | Filename remains `Air_Traffic_Passenger_Statistics_2005-2020.csv`; actual local activity periods are 2005-01–2025-07. GT6 has 21 annual rows, 2005–2025. | DataSF's dataset page identifies the Air Traffic Passenger Statistics dataset and PDDL metadata.[5][14] | Keep the supplied source filename and values unchanged; document that the local snapshot exceeds the filename's apparent end year. |
| CAA Table 12.1 | Project brief identifies the CAA source | The local route file has `this_period=202205`; its supplied prior-passenger fields have no separate prior-period code. | CAA Table 12.1 explicitly compares May 2022 with May 2021; the CAA page states an attribution/reference requirement and no-sale condition.[4][12] | Public narrative is corrected to May 2022 vs May 2021. The historical Cognos/Power BI screenshots that visibly say 2020 remain byte-for-byte unchanged and are flagged as mismatched; do not describe their label as the official source period. |

## Licensing and attribution matrix

| Material | Official rights evidence | Project treatment |
|---|---|---|
| Owner-authored code/software | Root [`LICENSE`](../../../LICENSE) remains MIT. | Keep MIT scoped to owner-authored Python, SQL and other software. It does not license third-party statistics, datasets, screenshot content, maps or vendor materials. |
| CAA Table 12.1 and CAA-derived statistics | CAA requires reference/attribution and says its statistics may not be sold on to a third party; its publication is not described here as OGL.[4] The official table states the May 2022 / May 2021 comparison.[12] | Apply CAA credit and no-sale condition to CAA-derived GT1–GT4/GT8 and related visuals. Do not claim MIT or unrestricted OGL rights. GT4's complete pair aggregation warrants particular caution; obtain rights-holder guidance before broader redistribution or commercial use. |
| DfT AVI0105 / CAA-origin material | DfT identifies CAA as the underlying source.[2] The current public DfT ODS is not the local 2013–2023 snapshot.[9] OGL v3.0 excludes third-party rights the provider is not authorised to license.[3] | Treat OGL as conditional on the exact material being made available under it and DfT having authority. Retain DfT/CAA attribution. Confirm the historical local table's specific licensing authority before making broad reuse claims; GT5 reproduces the full transformed local table. |
| SFO / DataSF | DataSF's metadata identifies PDDL; the PDDL v1.0 instrument states no restrictions or requirements are placed on the recipient by that instrument.[5][6][14] | Keep DataSF/SFO provenance and PDDL notice. GT6 is a derived annual aggregate of the entire local input, not a raw-row copy. |
| AVI0301 / ICAO | DfT identifies ICAO as the source; the current DfT edition is not the local 2021–2022 file.[2][10] ICAO DATA+ terms restrict publication of covered material without written authorization, but the local snapshot has not been linked to that exact product/edition.[7][8] | Rights remain unresolved. Do not declare ICAO data open-licensed or distribute raw AVI0301, GT7/GT9/GT10 mixed data outputs, global names/values/ranks/scores, or data-bearing screenshots until the exact edition and authoritative permission are confirmed. A DfT/ICAO credit alone is not a redistribution grant. |
| Owner-created screenshots and map layers | Owner authorization covers their report/design work, not third-party data. The inventory records visible map credits (OpenStreetMap, Microsoft, Esri); exact layer/provider terms still require review. | Assess every image individually. Do not exclude Cognos, Colab, Azure, Power BI or watsonx solely because a vendor UI appears. Preserve originals; account/infrastructure identifiers, unresolved global data, map terms, and the CAA period mismatch are distinct gates. |

**Dashboard authorship is not data permission:** original report composition and owner authorization do not automatically grant rights over third-party statistics, maps, or vendor assets displayed inside the dashboard. The citation/rights analysis is a source review, not legal advice.

## Screenshot and evidence handling

The 26 archive originals were SHA-256 matched byte-for-byte against their repository-path copies (including the local-only Dubai candidate). No original PNG or the source ZIP was changed. The per-image inventory assigns **4 candidate, 6 conditional, 11 hold, and 5 local-only** outcomes. It explicitly distinguishes non-data design evidence, conditional CAA/map content, unresolved AVI0301/ICAO data, period-label issues, and screenshots with visible account/infrastructure context. Classification is OCR/text-level; full-resolution human visual review remains a gate before any release. This classification does not change repository visibility or authorize publishing.

No global numerical rows or candidate names are transcribed in this report. Some data-bearing global screenshots remain in the existing evidence gallery; their presence is not rights clearance. This documentation PR does not authorize additional publication or modification of those assets.

## Documentation changes prepared

- Retained the root MIT `LICENSE` unchanged and clarified its code-only scope.
- Updated the existing `docs/data-sources-and-licensing.md` rather than duplicating its inventory.
- Added [`THIRD_PARTY_NOTICES.md`](../../../THIRD_PARTY_NOTICES.md) with separate CAA, DfT/OGL, DataSF/PDDL and AVI0301/ICAO treatment.
- Added [`outputs/golden/README.md`](../../../outputs/golden/README.md) with per-table row counts, fields, lineage, full-versus-derived assessment and rights conditions.
- Added [`docs/evidence/screenshot-release-inventory.md`](../screenshot-release-inventory.md) with an individual OCR-visible-content/privacy/rights status for each archive screenshot; existing evidence notes now link to it and flag the CAA period mismatch without editing image pixels.
- Linked notices, licensing details, golden-table inventory and reproducibility guidance from the main README.

Use the per-image [screenshot inventory](../screenshot-release-inventory.md) as the current status record. The inventory documents item-level conditions; it is not a grant of permission or clearance to publish the images.

## Pre-publication checks

| Check | Result |
|---|---|
| Source input provenance | Four local input files matched the source manifest's SHA-256 and size values. |
| Tracked data inventory | Exactly seven tracked golden CSVs; no raw source CSVs or GT7/GT9/GT10 CSV outputs tracked. |
| Golden-table reconciliation | GT1/GT2/GT3/GT4/GT5/GT6/GT8 reconstructions passed; zero mismatches at `rtol=1e-9`, `atol=1e-9`. |
| Screenshot integrity | The prior local audit matched all 26 archive originals to their repository copies. This PR contains no image, archive, dataset or other binary path; the original screenshot files remain unchanged. |
| Markdown links and anchors | 327 local Markdown links/anchors across 29 in-scope Markdown files; zero missing targets or anchors. |
| Embedded image paths | 38 Markdown image references checked; zero missing local image files. All 26 screenshot inventory target paths exist. |
| Citations/evidence | `sources.py verify --evidence` passed for all 12 Markdown documents with citations, with zero verification failures. The shared task ledger contains 17 sources, each with evidence quotes; expected warnings report ledger sources unused in individual documents. |
| Privacy/secret-pattern scan | All 18 documentation files in this PR were checked with common credential/token patterns; no matches were found. This does not clear screenshots: the image-by-image inventory still flags visible Azure account/resource context and unresolved third-party data/map rights. |
| CI scope | Workflow pins Python 3.11, guards raw/canonical/private outputs, compiles source/scripts/tests, and collects 45 tests: 11 self-contained tests run, 34 `requires_sources` tests excluded from public CI. |
| Local tests | With the existing project venv (Python 3.14.7), `compileall` passed and `pytest -q -m 'not requires_sources'` reported **11 passed, 34 deselected**. This is not an exact Python 3.11 CI run. |
| Diff hygiene | Staged diff, local path/anchor, image-path and citation/evidence checks are reported for the documentation PR branch. |
| Side effects | No repository visibility change, history rewrite, new repository, analytical-code/data change, screenshot alteration or cloud access. |

## Remaining owner/rights questions

1. Can DfT/CAA confirm the licence and redistribution authority for the exact local AVI0105 snapshot (2013–2023), including the fact that DfT identifies CAA as source?
2. What exact ICAO edition/file and access product produced the local AVI0301 2021–2022 values? Does an authoritative written permission cover the raw data, derived outputs, rankings and existing screenshots?
3. Does CAA's no-sale/attribution statement permit the intended noncommercial portfolio display of the complete GT4 aggregation, and what credit placement is required for each screenshot/figure?
4. Can the exact map layers used in the Power BI/Cognos screenshots be identified and their attribution/reuse terms confirmed?
5. Are the Azure SQL server endpoint, resource-group and subscription details visible in the historical screenshot still active or sensitive? If so, what separate privacy action is warranted while preserving the original image?
6. How should the existing screenshots with the 2020 label be captioned or contextualized if shown, without altering the originals?

## Publication and preservation boundary

The existing repository remains the canonical public portfolio project. This documentation PR contains no screenshot or data asset, does not change repository visibility and does not rewrite history. Preserve all original screenshots and project history. Owner approval of these documentation changes does not clear unresolved image-specific rights/privacy questions, authorize screenshot alteration, or establish permission to redistribute third-party material. Before any further reuse of a specific image, establish its source/permission and privacy basis independently. Do not remove or conceal existing evidence as part of this review.

## Sources

[2] https://www.gov.uk/government/publications/aviation-statistics-notes-and-definitions/aviation-statistics-notes-and-definitions — DfT Aviation statistics: notes and definitions
[3] https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3 — Open Government Licence v3.0
[4] https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2022/may-2022 — CAA UK airport data May 2022
[5] https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg/about_data — DataSF Air Traffic Passenger Statistics
[6] https://opendatacommons.org/licenses/pddl/1-0 — Open Data Commons PDDL v1.0
[7] https://dataplus.icao.int/Content/docs/terms_and_conditions.pdf — ICAO DATA+ Terms and Conditions
[8] https://dataplus.icao.int/Home/FAQ — ICAO DATA+ FAQ
[9] https://assets.publishing.service.gov.uk/media/6936e31a92da4705a575d42b/avi0105.ods — DfT AVI0105 ODS, updated 17 December 2025
[10] https://assets.publishing.service.gov.uk/media/6936e3a76a167b6884b73640/avi0301.ods — DfT AVI0301 ODS, updated 17 December 2025
[11] https://www.icao.int/presentation-2023-air-transport-statistical-results — ICAO 2023 Air Transport Statistical Results
[12] https://www.caa.co.uk/Documents/Download/9070/47d4f858-9581-43d1-9ee5-9aebfaf3c83e/5062 — CAA Table 12.1 May 2022 PDF, Comparison with May 2021
[14] https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg — DataSF Air Traffic Passenger Statistics dataset
