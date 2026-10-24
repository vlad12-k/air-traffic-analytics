# AirTrafficAnalytics

[![Python CI](https://github.com/vlad12-k/air-traffic-analytics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vlad12-k/air-traffic-analytics/actions/workflows/ci.yml)

**Evidence-driven airport expansion decision intelligence for a boutique retail business.** The project evaluates UK airport markets for a first boutique and separately frames international airports for possible later expansion. It is decision support—not a live airport service, sales forecast, commercial feasibility study, or investment recommendation.

## Executive overview

The business problem was to replace an informal “which airport looks promising?” discussion with an auditable comparison of passenger scale, market position, destination connectivity and scenario assumptions. The model separates the initial **UK_SITE** decision from the later **GLOBAL_EXPANSION** screen because their candidate populations and source data differ. Per the project owner, the IBM Cognos and Power BI dashboard/report designs and analysis were personally created for the academic work; IBM and Microsoft supplied the tools, not the analytical authorship. The college supplied dataset links and learning resources, which document access but do not grant redistribution rights.

The complete local project and canonical run remain preserved. This release candidate is rights-filtered: it excludes raw inputs, AVI0301/ICAO-derived global results and detailed QA outputs. It contains six original BI report captures, two Power BI schema originals, the owner-confirmed SIPOC original and one separately counted redacted Colab derivative; 17 of the 26 archive originals remain local-only under the specific boundaries in the evidence index.

## Authentic BI platform screenshots

The project owner states they created the Power BI and Cognos reports and analysis. The original PNGs below come from the supplied archive; they are not reconstructed or redacted. The owner's authorization to show their authored report work does not assert vendor permission or endorsement.

### Microsoft Power BI V2

#### UK airport demand

![Original Power BI V2 UK airport demand report page](docs/evidence/power-bi-v2/powerbi-v2-02-uk-market-demand.png)

*User-created demand report supporting the UK_SITE market-screening question. Source: UK CAA Table 12.1, May 2022. CAA requires source reference and prohibits resale; the screenshot also displays Power BI UI. No Microsoft endorsement or separate Microsoft permission is claimed for this data-bearing capture.*

#### UK_SITE scenario sensitivity

![Original Power BI V2 UK_SITE scenario sensitivity page](docs/evidence/power-bi-v2/powerbi-v2-05b-scenario-sensitivity-uk.png)

*User-created scenario analysis comparing UK_SITE ranking under the baseline, volume-heavy and connectivity-heavy policies. Source: UK CAA Table 12.1, May 2022; CAA source reference and no-resale conditions apply. This is a genuine Power BI capture, not the supplemental SVG result summary; no Microsoft permission or endorsement is claimed.*

#### Heathrow candidate detail

![Original Power BI V2 Heathrow candidate detail page](docs/evidence/power-bi-v2/powerbi-v2-07b-candidate-detail-heathrow.png)

*User-created candidate-detail report explaining the Heathrow UK_SITE screen using CAA-derived measures. Source: UK CAA Table 12.1, May 2022; CAA source reference and no-resale conditions apply. The screenshot contains Power BI UI; no Microsoft permission or endorsement is claimed.*

#### Semantic model and relationships

The two previously published, unchanged schema screenshots show the author's model design rather than airport data rows.

| Semantic model | Relationships |
|---|---|
| ![Microsoft Power BI semantic model overview](docs/evidence/power-bi-v2/powerbi-v2-08-semantic-model-overview.png) | ![Microsoft Power BI relationships overview](docs/evidence/power-bi-v2/powerbi-v2-09-relationships-overview.png) |

**Attribution on these two schema-only captures:** “Used with permission from Microsoft.” This is the standard published screenshot attribution for those data-free images; it is not an endorsement or a bespoke permission letter. The three CAA-based report pages above are included at the project owner's direction with the vendor-UI risk explicitly disclosed; the six remaining report pages are not included, as detailed in the [evidence index](docs/evidence/README.md).

### IBM Cognos Analytics — historical work

#### Semantic model

![Original IBM Cognos semantic-model screenshot](docs/evidence/historical/cognos/historical-cognos-07-semantic-model.png)

*The owner-created semantic-model view demonstrates historical Cognos model design. The original Cognos interface is visible; no IBM permission or endorsement is claimed.*

#### UK demand filter

![Original IBM Cognos UK demand-filter screenshot](docs/evidence/historical/cognos/historical-cognos-11-demand-filter.png)

*The owner-created report uses a UK airport filter to examine passenger demand. Source: UK CAA Table 12.1, May 2022; CAA attribution/no-resale conditions apply. IBM Cognos UI is visible; no IBM permission or endorsement is claimed.*

#### UK demand recovery

![Original IBM Cognos UK airport demand-recovery report](docs/evidence/historical/cognos/historical-cognos-10-demand-recovery-original.png)

*This authentic original shows a ten-airport UK comparison, period totals and recovery context. All ten displayed current/prior airport pairs match the preserved GT1 output derived from CAA Table 12.1, May 2022; the original Cognos query is not available. CAA attribution/no-resale conditions apply. No IBM endorsement is claimed.*

The three Cognos screenshots above are included at the project owner's direction; they reproduce IBM Cognos UI and do not claim IBM permission or endorsement. Five other Cognos captures remain local. `14-cognos-risk-ranking.png` contains populated airport rows and passenger, route, recovery and composite-score fields; its source lineage and redistribution rights are unresolved. The executive/global and populated operational pages remain local under the documented AVI0301/ICAO restrictions. See the [evidence index](docs/evidence/README.md) for each file and blocker.

The historical Colab, Azure SQL, watsonx and SIPOC screenshots are individually accounted for in the [historical engineering evidence gallery](docs/evidence/historical/README.md); the page distinguishes what the captures show from what is not reproducible or cleared for publication.

### Historical process design — SIPOC

![Original owner-authored SIPOC for airport site selection](docs/evidence/historical/process/01-business-process-sipoc.png)

*This original diagram records the intended input-to-decision workflow and GT1–GT10 outputs; it is process-design evidence, not proof every depicted step ran. See the [full historical technical notes](docs/evidence/historical/technical-notes.md).*

## Business questions

1. **UK_SITE:** Which UK airport market is strongest for further investigation as the first boutique location?
2. **GLOBAL_EXPANSION:** Which non-UK airport markets merit consideration after the first-site decision?

The intended decision owner is inferred to be the boutique owner or expansion leadership; analytics/BI users maintain the governed measures and reporting. The repository contains no formal stakeholder matrix or separate original academic report.

## Verified findings

The canonical UK analysis uses the CAA May 2022 route snapshot and its supplied comparison period. In the 36-airport population represented by the extract, Heathrow leads current passenger scale at **4.99 million** (**27.77%** of that represented total), with 90 destination countries and 207 destination airports recorded in GT8. The canonical UK_SITE baseline ranks Heathrow first and keeps it at the top across the three tested UK policy scenarios. These are reasons to prioritize further due diligence—not proof that a shop will be profitable.

![Original CAA-based UK airport market snapshot](docs/evidence/visualizations/uk-airport-market-snapshot.svg)

The CAA source requires attribution and prohibits resale; those conditions are recorded in the [data-source and licensing inventory](docs/data-sources-and-licensing.md). The SVG is an independently authored chart from permitted GT3 output, not a Power BI or Cognos screenshot.

![Heathrow demand and destination-connectivity snapshot using CAA data](docs/evidence/visualizations/uk-site-demand-connectivity.svg)

*An original, vendor-neutral view of Heathrow's CAA route passenger comparison and top destination-country flows. It addresses whether market scale is accompanied by route breadth; it is not retail footfall or a Power BI export. CAA attribution and no-resale conditions are embedded in the figure.*

AVI0105 adds country-level demand context: “Spain & Canary Islands” is the largest reported 2023 grouping, followed by the United States. This is not an airport-level recovery measure. The historical SFO series shows a large 2019–2020 disruption, but it is context only and ends in 2020.

![UK_SITE leader remains Heathrow across three tested policy scenarios](docs/evidence/visualizations/uk-site-scenario-stability.svg)

*Original rendering of the canonical UK-only sensitivity result. It shows the leading candidate, not scenario scores; the analysis tests policy-weight sensitivity, not probability or profitability.*

**Global expansion findings are not published.** AVI0301 is ICAO-sourced and its redistribution rights are unresolved; no global candidate names, scores, ranks or recommendations are reproduced here.

## Project evolution

- **Historical IBM Cognos Analytics:** the project owner personally created the semantic model and reports. Original captures of the model and UK demand filter are included at the owner's direction with no IBM permission or endorsement claimed; the recovery page has unresolved global data lineage, and the executive/operational/risk captures remain local under existing data restrictions.
- **Historical Colab / Python / Azure SQL:** the archive shows a notebook-based CSV-to-SQL upload and an Azure SQL result screen. One authentic Colab screenshot derivative is published with the entire upload-output block masked; the unredacted original and data-bearing Azure result remain local. Google Colab and Azure are historical tools, not claimed live services.
- **Current Python/SQL V2 analytical model:** modular ingestion, cleaning, GT1–GT10 contracts, source reconciliation, quality gates, model versioning and run provenance.
- **Power BI V2:** the owner's report pages cover executive decision, UK demand, connectivity, scenarios, candidate detail, governance and model relationships. Three original CAA-based report captures and the two previously published schema screenshots are shown; no Microsoft permission or endorsement is claimed for the three data-bearing captures. Remaining global and other report captures stay local.

The project shows sequential implementations of a similar business workflow; it does not claim a direct technical migration from Cognos to Power BI. For the detailed timeline and methods, see the [business case study](docs/business-case-study.md).

![Supplementary project chronology diagram, not platform-usage evidence](docs/evidence/visualizations/project-evolution-timeline.svg)

*Supplementary diagram summarized from project documents; it is not a software screenshot, report export, or proof of use of IBM Cognos, Google Colab, Azure SQL, Python/SQL V2, or Power BI.*

## Architecture and methodology

```text
Aviation source extracts
        ↓
Python ingestion, cleaning and standardisation
        ↓
Governed GT1–GT8 + GT10 decision model
        ↓
Quality checks, reconciliation, GT9, provenance
        ↓
SQL publication design (meta / bi / reporting)
        ↓
Power BI V2 report layer
```

GT1–GT8 capture UK market, comparison, destination, trend, benchmark and connectivity measures; GT9 records operational/data-quality KPIs; GT10 stores recommendations at candidate × decision scope × scenario × model version. UK_SITE and GLOBAL_EXPANSION are normalized and ranked independently. Scenarios vary explicit policy weights; their stability is sensitivity to assumptions, not statistical confidence. Detailed contracts and weights are in [`docs/gt-contracts.md`](docs/gt-contracts.md) and [`docs/decision-model.md`](docs/decision-model.md).

## Data governance and validation

The canonical local run `20261005T163644Z_33f9f4ffa323` is recorded as `VALIDATED_LOCAL`. Its QA record reports 30 checks, zero failures and zero warnings. Source/artifact manifests in the public candidate contain paths, sizes and hashes only; sample rows, row-level QA, candidate-level files and Azure result logs are local-only. The manifest entries were checked against the preserved local run by size and SHA-256.

Azure SQL schema, reporting-view and validation scripts are included, but no live Azure operation was performed for this case study. The archived run and screenshot evidence are not claims of a currently deployed or refreshing Azure, Power BI, Cognos or watsonx service.

## Continuous integration

The GitHub Actions workflow is configured for Python 3.11 on pushes to `main`, pull requests targeting `main`, and manual dispatch. It installs the locked environment with `uv sync --locked --extra dev`, compiles `src/`, `scripts/` and `tests/`, and runs the self-contained test subset. The public CI job will report source-dependent tests as not executed, not passed. No test contacts Azure or another external service; Azure configuration tests only build a connection-string value.

The repository's suite currently collects **45** tests: **11** are self-contained and run in public CI; **34** are marked `requires_sources` because they call the canonical ingestion/analytics path and need local CSV inputs. The public subset consists of pure configuration/ODBC normalization tests in `test_azure_config.py` and the synthetic AVI0301-cleaning unit test in `test_clean.py`; its AVI0301 example values are artificial, not aviation rows. The source-dependent cases are in `test_clean.py`, `test_ingest.py`, `test_gt4_null_semantics.py`, `test_golden_tables.py`, `test_quality.py`, `test_scoring.py`, `test_pipeline.py` and `test_numeric_finiteness.py`.

For a clean checkout, install from the lock and run the same public-safe checks:

```bash
uv sync --locked --extra dev
uv run python -m compileall -q src scripts tests
uv run pytest -q -m "not requires_sources"
```

With all four source files named in `src/airtraffic/config.py` lawfully available under `data/raw/`, run the complete local suite with `uv run pytest -q`. They are not bundled in the public repository; AVI0301/ICAO rights remain unresolved, so clean-clone reproduction of the full pipeline is intentionally unavailable. The CI badge at the top is scoped to `main`; the current PR check and test scope are reported by GitHub Actions.

## Reproducibility, licensing and limitations

The Python package requires four CSV inputs under `data/raw/`; none are bundled. Full pipeline/tests therefore require lawfully obtained local source files. AVI0301/ICAO rights are unresolved, so a clean clone cannot reproduce the global benchmark or complete run until those rights and a lawful input path are settled. The local test suite passed **45 tests** with the local source environment; coverage is not configured.

CAA Table 12.1 must be attributed and may not be resold; DfT AVI0105 carries OGL/source-note conditions; DataSF identifies the SFO dataset as PDDL 1.0. The MIT `LICENSE` covers original code only—not datasets, derived third-party statistics, screenshots or other publisher materials. See [`docs/data-sources-and-licensing.md`](docs/data-sources-and-licensing.md) and [`docs/reproducibility.md`](docs/reproducibility.md).

Other limitations: sources are historical snapshots; CAA route data is one comparison snapshot, not a multi-year airport history; AVI0105 is country-level; SFO is an external historical comparator ending in 2020; the global benchmark is limited to AVI0301's source population; and the model omits commercial inputs such as rent, retail conversion, available premises and operating margin. Rankings are comparative screens, not forecasts or proof of viability.

## Documentation

- [Business case study](docs/business-case-study.md)
- [End-to-end project walkthrough](docs/end-to-end-project-walkthrough.md)
- [Power BI V2 original screenshot gallery and technical notes](docs/evidence/power-bi-v2/technical-notes.md)
- [Historical engineering evidence gallery](docs/evidence/historical/README.md)
- [Historical screenshot technical notes](docs/evidence/historical/technical-notes.md)
- [Architecture](docs/architecture.md)
- [Analytical lineage](docs/lineage.md)
- [GT1–GT10 contracts](docs/gt-contracts.md)
- [Decision model](docs/decision-model.md)
- [Data sources and licensing](docs/data-sources-and-licensing.md)
- [Evidence and local-only screenshot indexes](docs/evidence/)
