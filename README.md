# AirTrafficAnalytics — Airport Expansion Decision Intelligence

[![Python CI — main](https://github.com/vlad12-k/air-traffic-analytics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/vlad12-k/air-traffic-analytics/actions/workflows/ci.yml?query=branch%3Amain)

**An evidence-led data and BI case study for screening airport markets for a boutique retailer.** I designed a Python/SQL analytical workflow and decision model, then presented the work through Power BI. Earlier Cognos, Colab, Azure SQL and watsonx/AutoAI work is documented as historical project evidence—not as a live commercial service or invented employment experience.

## The business question

Which UK airport market merits further investigation for a first boutique, and which non-UK markets could be screened separately for possible later expansion? Passenger volume alone is not a site decision: route breadth, source periods, candidate eligibility and explicit policy assumptions also matter. The model keeps **UK_SITE** and **GLOBAL_EXPANSION** as separate populations and decisions.

## What I built

| Area | Work evidenced in this repository |
|---|---|
| Data engineering | Python source ingestion, source-specific cleaning, governed GT1–GT10 outputs, metadata manifests and run provenance |
| Analytics engineering | Explicit table grains, lineage, quality gates, reconciliation and versioned scenario weights |
| Decision modelling | Separate UK/global candidate eligibility and within-scope score normalisation; UK sensitivity across three policy profiles |
| BI | Personally authored Power BI V2 and historical IBM Cognos report/model designs, with evidence boundaries documented per screenshot |
| Historical exploration | Colab ETL, Azure SQL workflow and watsonx/AutoAI screens, clearly distinguished from the current Python/SQL implementation |

**Tools by purpose:** Python and pandas for transformation; SQL/T-SQL for analytical storage and reporting design; Power BI and Cognos for BI; Colab, Azure SQL and watsonx/AutoAI in historical project stages. The repository does not claim a currently deployed cloud service.

## Selected original dashboard evidence

### Power BI — executive decision view

![Original Power BI V2 executive decision summary](docs/evidence/power-bi-v2/powerbi-v2-01-executive-decision-summary-original.png)

*The report separates the UK first-site screen from the historical global-expansion view. The screenshot records a past report state; global values are not presented here as current or independently revalidated results.*

### Power BI — UK airport demand

![Original Power BI V2 UK market demand report](docs/evidence/power-bi-v2/powerbi-v2-02-uk-market-demand.png)

*The CAA-based page compares the represented UK airport population and selected-market demand. It supports market screening, not retail footfall or a lease decision.*

### Power BI — scenario sensitivity

![Original Power BI V2 UK_SITE scenario sensitivity page](docs/evidence/power-bi-v2/powerbi-v2-05b-scenario-sensitivity-uk.png)

*The UK leader remains the same across baseline, volume-heavy and connectivity-heavy policies. This is sensitivity to chosen weights, not a probability or profitability estimate.*

### IBM Cognos — historical executive view

![Original IBM Cognos executive summary](docs/evidence/historical/cognos/historical-cognos-08-executive-summary-original.png)

*An original historical report design combining UK/global views and recovery context. Its original query definitions are not available, so the image is not evidence of a current refresh or a fully reproducible calculation.*

The source archive contains **26 originals**: 11 Power BI, eight Cognos and seven historical engineering/process images. The public inline galleries publish **25** (10 Power BI, eight Cognos and seven historical). The genuine Dubai 07a Power BI original remains local-only: it displays AVI0301/ICAO-derived candidate metrics, and its source-rights and screenshot conditions are unresolved. The [evidence index](docs/evidence/README.md) distinguishes published originals, the local-only archive item, the redacted Colab derivative and duplicate model-view copies.

## Evidence-backed UK finding

The UK_SITE screen represents **36 airports** in UK CAA Table 12.1 (May 2022; source period `202205`, with the extract's supplied 2022-versus-2020 comparison—not a continuous annual series). The current-period represented total is **17,984,754** passengers; the supplied prior-period total is **1,178,740**. Heathrow records **4,993,568** current-period passengers, or **27.77% of the 17,984,754 represented current-period total**, and remains the leading UK candidate in all three documented scenarios.

This supports taking Heathrow forward for **further commercial due diligence**. It does not establish airport retail footfall, available premises, rent, customer conversion, profitability or investment return. Historical international dashboard values remain screenshot evidence; no current global candidate ranking is asserted in prose.

## How it works

```text
Source extracts (locally obtained)
  → Python ingestion, cleaning and profiling
  → governed GT1–GT8 measures and GT10 scope/scenario decisions
  → quality checks, reconciliation, GT9 and run provenance
  → SQL publication design
  → Power BI V2 decision reporting
```

The full implementation sequence—including SIPOC, historical Colab/Azure SQL, Cognos and watsonx/AutoAI stages—is in the [engineering walkthrough](docs/end-to-end-project-walkthrough.md). Current V2 code is a later, separately documented implementation; it is **not** described as an automated Cognos-to-Power-BI migration.

## Validation and limits

The archived canonical local run is recorded as `VALIDATED_LOCAL`, with **30 checks, zero failures and zero warnings**; that run was not regenerated for this release. Public CI is configured to run **11 source-independent tests**. A further **34 tests** require four local CSV inputs and are not run by public CI. The repository contains no raw source CSVs, credentials or live cloud connection; a clean clone therefore cannot reproduce the full source-backed pipeline.

CAA Table 12.1 attribution and no-resale conditions apply. DfT and DataSF sources retain their own terms; AVI0301/ICAO rights remain unresolved and raw/global output tables stay excluded. The MIT licence covers original code only. See [sources and licensing](docs/data-sources-and-licensing.md) and [reproducibility](docs/reproducibility.md).

## Explore the project

- **Business story:** [Business case study](docs/business-case-study.md)
- **How it works:** [Engineering walkthrough](docs/end-to-end-project-walkthrough.md) · [Architecture](docs/architecture.md) · [Decision model](docs/decision-model.md) · [GT1–GT10 contracts](docs/gt-contracts.md) · [Lineage](docs/lineage.md)
- **See the dashboards:** [Power BI gallery](docs/evidence/power-bi-v2/technical-notes.md) · [Cognos gallery](docs/evidence/historical/cognos/technical-notes.md)
- **Historical engineering work:** [Colab, Azure SQL, watsonx and SIPOC gallery](docs/evidence/historical/README.md) · [technical notes](docs/evidence/historical/technical-notes.md)
- **Inspect the implementation:** [Python package](src/airtraffic/) · [SQL](sql/) · [tests](tests/) · [GitHub Actions workflow](.github/workflows/ci.yml)
- **Reproduce public checks:** [reproducibility guide](docs/reproducibility.md) · run history and scope in [Actions](https://github.com/vlad12-k/air-traffic-analytics/actions/workflows/ci.yml?query=branch%3Adocs%2Ffinal-bi-case-study)
- **Complete evidence inventory:** [26-original screenshot index](docs/evidence/README.md)
