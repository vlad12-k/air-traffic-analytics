# AirTrafficAnalytics — Airport Expansion Decision Intelligence

[![Python CI — main](https://github.com/vlad12-k/air-traffic-analytics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vlad12-k/air-traffic-analytics/actions/workflows/ci.yml?query=branch%3Amain)

**This existing repository is the canonical portfolio project; the work below documents it rather than creating a separate portfolio repository or reconstructed release.**

**An individual academic and portfolio project about turning airport-traffic data into a documented BI workflow for airport retail-location screening.** It began as a Unit 19 Business Intelligence assessment and later developed into a separately documented Python/SQL V2 implementation. No employment by a scenario organisation or commercial deployment is claimed.

## Academic origin and scenario

The assignment brief supplied a fictional business case: **RCO Data Services Ltd (RDS)** advises the fictional **Luxury Watch Company (LWC)** on airport retail-location decision support. The brief identified learning resources and aviation datasets; access through a college brief does not grant unlimited rights to republish those datasets. The complete assignment brief is not reproduced here.

My individual contribution spans data acquisition and profiling, Python/pandas preparation, Google Colab ETL, Golden Tables GT1–GT10, SQL and historical Azure SQL workflows, IBM Cognos Analytics modelling/reporting, IBM watsonx AutoAI exploration, Microsoft Power BI dashboards, and later data-quality, reconciliation, provenance and decision-modelling work. Historical tool screenshots document past work; they do not prove that a cloud service is live today. See [academic provenance](docs/academic-provenance.md) for the boundary between the academic stage and later V2 work.

## Decision question

Which represented UK airport merits further investigation for a first boutique, and which non-UK airports could be screened separately for possible later expansion? Passenger counts are market context—not retail footfall, premises availability, sales, profitability or investment return. The model keeps **UK_SITE** and **GLOBAL_EXPANSION** as separate populations, lineages and decisions.

## Project workflow and implementation

```text
Academic business question and source review
  → source acquisition, profiling and period checks
  → historical Python / pandas and Colab ETL
  → Golden Tables and historical Azure SQL workflow
  → historical Cognos modelling/reporting and watsonx AutoAI exploration
  → later Python/SQL V2 with contracts, tests, reconciliation and provenance
  → Power BI V2 decision reporting
```

These are successive approaches to the question, not an automated Cognos-to-Power-BI migration. Current Python/SQL code does not retroactively validate an earlier notebook, Azure result grid, Cognos report or AutoAI experiment.

| Area | Evidence in this repository |
|---|---|
| Data engineering | Python and pandas ingestion/cleaning; source-specific handling; run metadata and provenance |
| Analytics engineering | Explicit GT1–GT10 grains, source lineage, data-quality checks and reconciliation |
| Decision modelling | Separate UK/global eligibility and scope-specific scoring; three UK policy-weight sensitivity profiles |
| SQL | T-SQL/SQL publication design and validation queries; historical Azure SQL screenshots are not proof of a currently running service |
| BI | Owner-authored Power BI V2 pages and historical IBM Cognos model/report screenshots |
| Exploratory modelling | Historical watsonx AutoAI experiment screens; no exported model, independently validated holdout result or deployment is claimed |

## Golden Tables and analytical contracts

| Tables | Grain / role | Source lineage and publication boundary |
|---|---|---|
| GT1–GT3 | One row per represented UK airport: period totals, change and market rank/share | CAA Table 12.1, May 2022 compared with May 2021; attribution and published no-sale conditions apply.[4][12] |
| GT4 | UK airport × destination country | Complete aggregation of the local CAA route-pair domain; substantial source-derived output, not a small sample. Attribution and no-sale terms apply.[4][12] |
| GT5 | Source category × year | Local DfT AVI0105 snapshot, 2013–2023; transformed values reproduce all local category/year passenger cells. DfT/CAA authority and OGL exceptions remain relevant.[1][2][3] |
| GT6 | Year | Annual aggregate of local DataSF/SFO data, activity periods 2005-01–2025-07; dataset metadata identifies PDDL 1.0.[5][6][14] |
| GT7 | Global airport benchmark | DfT AVI0301 / ICAO lineage; exact local originating edition and redistribution permission are unresolved.[2][3][10] |
| GT8 | One row per represented UK airport | CAA route connectivity and scheduled/charter context; attribution/no-sale conditions apply.[4][12] |
| GT9 | Run × KPI | Mixed operational/coverage measures; not among the seven tracked golden CSVs |
| GT10 | Candidate × decision scope × scenario × model version | Scope-specific recommendation/scenario contract; not among the seven tracked golden CSVs |

Only **GT1, GT2, GT3, GT4, GT5, GT6 and GT8** are tracked as `outputs/golden/*.csv`. GT7/GT9/GT10 data outputs and raw source CSVs are not tracked there, although some historical screenshots visibly contain global or mixed-source results. The [golden-table inventory](outputs/golden/README.md) documents the exact tracked files, row counts, reconciliation basis and source boundaries.

## Method and findings

The CAA source extract represents **36 airports**. Its `202205` current period is May 2022, compared with the source-provided May 2021 period—not 2020 and not a continuous annual series. In this snapshot, the represented current-period total is **17,984,754**; Heathrow records **4,993,568** (27.77% of that represented total) and leads the UK_SITE screen across the three documented policies. The recommendation is to carry Heathrow forward for further due diligence, not to select or lease a retail unit.[4][12]

UK_SITE scenario weights are explicit policy choices for passenger scale, destination-country breadth and destination-airport breadth. GLOBAL_EXPANSION uses a separate AVI0301-linked population and separate within-scope scoring. The latter's source edition and rights are unresolved, so this README does not publish a current or validated global winner.[2][3][10] Scenario stability is sensitivity to selected assumptions, not probability, forecast accuracy or profitability.

The Power BI UK-demand capture and original Cognos demand captures visibly label the comparison **2020 vs 2022**. That historical label conflicts with the verified CAA May 2021 vs May 2022 source period.[12] The images remain unchanged; see the [Power BI capture note](docs/evidence/power-bi-v2/technical-notes.md), [Cognos capture note](docs/evidence/historical/cognos/technical-notes.md) and [per-image screenshot inventory](docs/evidence/screenshot-release-inventory.md). Do not treat the old label as the official CAA period.

## Data quality, reconciliation and tests

The archived canonical local run is recorded as `VALIDATED_LOCAL` with **30 checks, zero failures and zero warnings**; that run was not regenerated for this documentation work. The tracked CAA-derived golden tables reconcile to local source inputs; GT4 covers all 666 unique airport-country pairs, and the tracked GT5 values match all 847 local category/year passenger cells after the documented unit conversion. These checks support the V2 outputs only; they are not validation of historical Cognos, Colab, Azure or AutoAI screens.

Public CI is configured for **11 source-independent tests**. The full local test suite collects 45 tests; 34 require four local CSV inputs and are not run by public CI. The current repository does not bundle those raw source files or credentials. A clean clone therefore cannot reproduce the complete source-backed pipeline. See [reproducibility](docs/reproducibility.md) and the [historical validation summary](docs/evidence/validation/release-validation-summary.md).

## Original report and process evidence

The existing galleries preserve the Power BI, Cognos, Colab, Azure SQL, watsonx/AutoAI and SIPOC screenshots and distinguish original files from the separately identified redacted Colab derivative. Captions describe what each image does—and does not—demonstrate. Three UK-only Power BI pages, one Cognos semantic-model image, and the redacted Colab derivative received owner full-resolution visual review in the prior evidence assessment; that visual assessment is **not** a legal permission or rights clearance. Other original images have OCR-level descriptions, not a completed pixel-by-pixel review.

**Existing public-evidence notice:** the public `main` branch already contains historical screenshots, including Azure account/resource context and screenshots with AVI0301/ICAO-associated global values. This documentation pass does not remove, alter, republish or newly clear those images. Account/infrastructure visibility and unresolved embedded-data rights are item-specific concerns; a vendor interface alone is not a prohibition, and a disclaimer alone does not resolve an actual privacy or rights issue. See the [26-original evidence index](docs/evidence/README.md) and [individual inventory](docs/evidence/screenshot-release-inventory.md) before any further reuse or publication decision.

## Dataset periods and reproducibility boundaries

| Dataset | Assignment / local / current-publication distinction |
|---|---|
| CAA Table 12.1 | Local source code `202205`; official table compares May 2022 with May 2021. Preserve this period in all narrative; do not edit historical screenshot pixels.[4][12] |
| DfT AVI0105 | Owner-provided assignment brief states 2011–2021; local file contains 2013–2023; the currently linked official ODS is a later 2014–2024 snapshot. No acquisition date for the local file is recorded.[1][2][9] |
| DfT AVI0301 | Assignment brief states 2019–2020; local file contains 2021–2022; current public DfT material is a later edition. The originating ICAO edition and redistribution permission for the local snapshot are unresolved.[2][3][10] |
| DataSF SFO | The supplied local filename says 2005–2020, but its observed activity-period coverage extends through 2025-07. The source file and name are left unchanged.[5][6][14] |

The current GitHub Actions workflow does not contact Azure, Cognos, watsonx, Colab or Power BI and does not refresh historical outputs. No current cloud resource, scheduled refresh, deployed ML model, reproducible historical Cognos package, commercial client, or production service is claimed.

## Licensing and source attribution

The root MIT `LICENSE` is retained for original owner-authored software only. It does **not** relicense third-party data, statistics, map layers, software interfaces, screenshots or vendor assets.

CAA attribution/no-sale terms are distinct from DfT/OGL, whose third-party-rights exception remains relevant.[2][3][4]

DataSF metadata identifies PDDL for dataset `rkru-6vcg` only.[5][6][14]

AVI0301/ICAO lineage and redistribution permission remain unresolved.[2][3][10]

Microsoft, IBM and Google product names identify historical tools; no vendor sponsorship or endorsement is implied, and no blanket screenshot permission is claimed.[15][16][17]

See [Third-Party Notices](THIRD_PARTY_NOTICES.md), [source and licensing details](docs/data-sources-and-licensing.md), [academic provenance](docs/academic-provenance.md), and the [image-by-image evidence inventory](docs/evidence/screenshot-release-inventory.md). The original Pearson assignment brief is not reproduced here; academic access to learning resources does not establish third-party publication rights.

## Explore

- **Business case:** [decision context and findings](docs/business-case-study.md)
- **Architecture and implementation:** [walkthrough](docs/end-to-end-project-walkthrough.md) · [architecture](docs/architecture.md) · [decision model](docs/decision-model.md) · [GT contracts](docs/gt-contracts.md) · [lineage](docs/lineage.md)
- **Reports and screenshots:** [Power BI gallery](docs/evidence/power-bi-v2/technical-notes.md) · [Cognos gallery](docs/evidence/historical/cognos/technical-notes.md) · [historical engineering gallery](docs/evidence/historical/README.md)
- **Code and validation:** [Python package](src/airtraffic/) · [SQL](sql/) · [tests](tests/) · [GitHub Actions](.github/workflows/ci.yml)
- **Data and licensing:** [source matrix](docs/data-sources-and-licensing.md) · [third-party notices](THIRD_PARTY_NOTICES.md) · [tracked golden tables](outputs/golden/README.md)

## Official source links

- UK CAA: [May 2022 airport data](https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2022/may-2022/) · [Table 12.1 PDF](https://www.caa.co.uk/Documents/Download/9070/47d4f858-9581-43d1-9ee5-9aebfaf3c83e/5062)
- DfT: [AVI tables landing page](https://www.gov.uk/government/statistical-data-sets/aviation-statistics-data-tables-avi) · [AVI0105 current ODS](https://assets.publishing.service.gov.uk/media/6936e31a92da4705a575d42b/avi0105.ods) · [AVI0301 current ODS](https://assets.publishing.service.gov.uk/media/6936e3a76a167b6884b73640/avi0301.ods) · [notes and definitions](https://www.gov.uk/government/publications/aviation-statistics-notes-and-definitions/aviation-statistics-notes-and-definitions) · [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3). The current ODS files are not asserted to be the historical local snapshots.
- DataSF: [Air Traffic Passenger Statistics, dataset `rkru-6vcg`](https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg/about_data) · [PDDL 1.0](https://opendatacommons.org/licenses/pddl/1-0/)
- ICAO reference material: [2023 Air Transport Statistical Results](https://www.icao.int/presentation-2023-air-transport-statistical-results) · [DATA+ terms](https://dataplus.icao.int/Content/docs/terms_and_conditions.pdf). These links do not identify the exact edition of the local AVI0301 input.
- Vendor guidance: [Microsoft copyright permissions](https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions) · [IBM copyright/trademark](https://www.ibm.com/legal/copyright-trademark) · [Google brand guidance](https://about.google/brand-resource-center/guidance/)

## Sources

[1] https://www.gov.uk/government/statistical-data-sets/aviation-statistics-data-tables-avi — DfT Aviation statistics: data tables (AVI)
[2] https://www.gov.uk/government/publications/aviation-statistics-notes-and-definitions/aviation-statistics-notes-and-definitions — DfT Aviation statistics: notes and definitions
[3] https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3 — Open Government Licence v3.0
[4] https://www.caa.co.uk/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-2022/may-2022 — CAA UK airport data May 2022
[5] https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg/about_data — DataSF Air Traffic Passenger Statistics
[6] https://opendatacommons.org/licenses/pddl/1-0 — Open Data Commons PDDL v1.0
[9] https://assets.publishing.service.gov.uk/media/6936e31a92da4705a575d42b/avi0105.ods — DfT AVI0105 ODS, updated 17 December 2025
[10] https://assets.publishing.service.gov.uk/media/6936e3a76a167b6884b73640/avi0301.ods — DfT AVI0301 ODS, updated 17 December 2025
[12] https://www.caa.co.uk/Documents/Download/9070/47d4f858-9581-43d1-9ee5-9aebfaf3c83e/5062 — CAA Table 12.1 May 2022 PDF, Comparison with May 2021
[14] https://data.sfgov.org/Transportation/Air-Traffic-Passenger-Statistics/rkru-6vcg — DataSF Air Traffic Passenger Statistics dataset
[15] https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions — Use of Microsoft Copyrighted Content
[16] https://www.ibm.com/legal/copyright-trademark — IBM Copyright and Trademark Information
[17] https://about.google/brand-resource-center/guidance — Google Brand Resource Center Guidance
