# AirTrafficAnalytics — engineering walkthrough

This walkthrough follows the project’s documented evolution from the business question and process design to historical tool work, the governed Python/SQL V2 implementation and Power BI reporting. It distinguishes original screenshot evidence from executable code and from current cloud resources. It does **not** claim an automated Cognos-to-Power-BI migration or a live deployment.

**Quick links:** [business case study](business-case-study.md) · [architecture](architecture.md) · [GT1–GT10 contracts](gt-contracts.md) · [decision model](decision-model.md) · [lineage](lineage.md) · [reproducibility](reproducibility.md) · [all screenshot evidence](evidence/README.md)

## Project lifecycle

**Business requirements and SIPOC → local data acquisition/profiling → historical Colab ETL and Azure SQL work → historical Cognos reporting and watsonx/AutoAI exploration → governed Python/SQL V2 → GT1–GT10 contracts → quality, reconciliation and versioned scenario scoring → Power BI V2 decision reporting.** These are successive implementations and evidence stages; the current V2 code does not retroactively validate earlier screenshots.

## 1. Business question and process design

The individual academic and portfolio project frames two decisions:

- **UK_SITE:** Which airport in the represented UK population merits further investigation for a first boutique?
- **GLOBAL_EXPANSION:** Which non-UK airport markets could be screened separately for possible later expansion?

The [Business Case Study](business-case-study.md) explains why passenger volume alone is insufficient: airport traffic does not measure retail footfall, premises, rent, conversion or unit economics. The intended decision owner is inferred from the documented problem; the repository has no formal stakeholder matrix or original requirements deck.

The original [SIPOC screenshot](evidence/historical/process/01-business-process-sipoc.png) documents intended inputs, stages and outputs, including GT1–GT10 and decision-pack review. It is process-design evidence, not proof that every depicted step ran. See the [SIPOC notes](evidence/historical/process/README.md).

## 2. Data acquisition and profiling

The current package reads four local CSV inputs configured in [`src/airtraffic/config.py`](../src/airtraffic/config.py). It does not download them, and the public repository does not bundle raw rows.

| Source | Role | Public boundary |
|---|---|---|
| AVI0105 | Country-level UK international passenger context | Local input only; DfT source/table terms apply. |
| AVI0301 | Global airport benchmark and GLOBAL_EXPANSION features | DfT notes identify ICAO lineage; exact originating edition/terms are unresolved. Raw rows and global output tables remain excluded. |
| CAA ROUTES / Table 12.1 | UK passenger comparison, airport–destination flows and connectivity | May 2022 source snapshot; attribution and the CAA no-resale condition apply. |
| SFO/DataSF | Separate historical airport-traffic benchmark | Ends in 2020; not a direct UK-market proxy. |

[`scripts/inspect_sources.py`](../scripts/inspect_sources.py) profiles row/column counts, types, nulls, duplicates and sample rows; it can print restricted source rows and is intended only for lawful local use. [`ingest.py`](../src/airtraffic/ingest.py) reads the configured files. Source periods, lineage and terms are summarised in [data sources and licensing](data-sources-and-licensing.md).

## 3. Historical Colab ETL and Azure SQL work

The [historical engineering gallery](evidence/historical/README.md) displays both original Colab/Azure SQL screenshots inline. The Colab capture shows a notebook-based CSV handoff using pandas, SQLAlchemy/ODBC and `DataFrame.to_sql(..., if_exists='replace')`; this replaces target tables on rerun. The screenshot does not show transaction-safe publication, a quality gate or complete source-target reconciliation. The notebook itself is not in the repository.

The Azure SQL captures show a historical database/resource context and a result grid. They do not establish that a service is currently running or that the displayed results were independently reconciled. The present repository contains a separate SQL publication design:

- [`sql/schema.sql`](../sql/schema.sql) defines run-aware `meta`, `bi` and `reporting` structures.
- [`sql/views.sql`](../sql/views.sql) defines views over the latest `PUBLISHED` run.
- [`sql/validation_queries.sql`](../sql/validation_queries.sql) provides post-publication reconciliation queries.
- [`scripts/apply_schema.py`](../scripts/apply_schema.py), [`scripts/apply_views.py`](../scripts/apply_views.py) and [`scripts/validate_published_run.py`](../scripts/validate_published_run.py) operate on an Azure SQL connection; [`scripts/publish_validated_run.py`](../scripts/publish_validated_run.py) can publish a validated local run.

These scripts can access or change external resources and require credentials. No Azure operation was performed for this portfolio; the SQL is a deployable design, not evidence of a live database.

## 4. Historical Cognos and watsonx/AutoAI exploration

The project owner reports personally creating the Cognos reports and semantic model. The [complete Cognos gallery](evidence/historical/cognos/technical-notes.md) shows all eight original captures in report sequence: semantic model, UK demand/recovery, executive views, operational monitoring/filtering and risk ranking. A local comparison found that all ten current/prior passenger pairs in the two UK demand views match the preserved GT1 output derived from CAA Table 12.1; this does not recover the original Cognos queries, joins, scoring or refresh path.

The [historical watsonx screenshots](evidence/historical/README.md) record asset selection and AutoAI pipeline-comparison views. They do not include an exported experiment, reproducible training data, an independent holdout evaluation or a deployed model. No forecasting accuracy or business outcome is inferred from the screenshot metrics.

These are historical project stages. Current V2 code is not described as a direct or automated migration from Cognos.

## 5. Governed Python/SQL V2 implementation

The current local execution path in [`pipeline.py`](../src/airtraffic/pipeline.py) is:

1. Load the four configured local sources.
2. Apply source-specific transformations in [`clean.py`](../src/airtraffic/clean.py).
3. Construct UK and global analytical tables in [`golden.py`](../src/airtraffic/golden.py).
4. Build eligibility, scope-specific features and GT10 scenarios in [`scoring.py`](../src/airtraffic/scoring.py).
5. Run reconciliation and publication-quality checks in [`quality.py`](../src/airtraffic/quality.py); stop on error-level gate failures.
6. Record run metadata/manifests in [`provenance.py`](../src/airtraffic/provenance.py) and write run-specific exports through [`export.py`](../src/airtraffic/export.py).

The [architecture](architecture.md) and [lineage](lineage.md) documents map these stages to SQL and BI consumers. The root-level legacy `main.py` prototype is not the canonical implementation; [`src/airtraffic/`](../src/airtraffic/) is.

## 6. GT contracts, decision scopes and scenario weights

The GT contracts are the governed interface between Python transformations, SQL and BI consumers:

| Contract | Responsibility | Main source |
|---|---|---|
| GT1 | UK airport current/prior passenger totals | CAA ROUTES |
| GT2 | UK period change and zero-baseline context | GT1 / CAA ROUTES |
| GT3 | Full represented UK population, market share and rank | GT1 |
| GT4 | Airport × destination-country flow | CAA ROUTES |
| GT5 | Country × year passenger trend context | AVI0105 |
| GT6 | Historical SFO benchmark | SFO/DataSF |
| GT7 | Global airport passenger/movement benchmark | AVI0301; raw rows excluded |
| GT8 | UK connectivity and scheduled/charter mix | CAA ROUTES |
| GT9 | Per-run operational, coverage and quality KPIs | Quality report and governed tables |
| GT10 | Candidate × scope × scenario × model version | Scope-specific model inputs |

UK_SITE uses within-scope percentile components for passenger scale and destination breadth. Its BASELINE / VOLUME_HEAVY / CONNECTIVITY_HEAVY weights are **0.50/0.30/0.20**, **0.65/0.20/0.15** and **0.35/0.35/0.30**. Period growth is contextual because small/zero denominators can create extreme ratios.

GLOBAL_EXPANSION is a separate candidate population with a deterministic eligibility check to exclude UK airports, its own normalisation and policies for passenger scale, growth, movement scale and passengers per movement. These two scopes are not compared on a shared score scale. Full feature definitions, policy weights and caveats are in the [decision model](decision-model.md); table grain and semantics are in the [GT contracts](gt-contracts.md).

## 7. Quality gates, reconciliation and provenance

The pipeline checks counts/components and source coverage before publication. `assert_publishable()` is called before export; run identity and metadata are attached by the provenance/export modules. The SQL validation queries are an independent post-publication check design, not evidence that a database was queried for this release.

The archived canonical run `20261005T163644Z_33f9f4ffa323` is recorded as `VALIDATED_LOCAL`, with **30 checks, zero failures and zero warnings**. This is historical local-run evidence, not a run regenerated while preparing these documents. Public manifests contain path/size/hash metadata only; data-bearing canonical outputs and raw source files remain local. See the [release validation summary](evidence/validation/release-validation-summary.md).

## 8. Power BI V2 decision reporting

The owner reports personally authoring the Power BI V2 report design and analysis. The [public Power BI gallery](evidence/power-bi-v2/technical-notes.md) embeds **10 of the 11** original archive screenshots and maps each displayed page to its visible purpose, current GT contracts/code where supported, and evidence limits. The Dubai 07a original remains local-only because it shows AVI0301/ICAO-derived candidate metrics and its source-rights/screenshot conditions are unresolved. The published pages cover UK demand, connectivity, scenarios, Heathrow candidate detail, quality/governance, global-scope overviews and model structure.

The report screenshots do not constitute a machine-readable semantic model, prove every relationship/measure, or show a current refresh. No `.pbix`, `.pbit`, report export or live Power BI service is included or claimed. The visual evidence documents successive work, not a Cognos migration.

## 9. Tests and reproduction boundary

The collected suite contains **45 tests**. Public CI runs **11 self-contained tests**; **34 tests** marked `requires_sources` need the four locally obtained CSVs and are not run in public CI. Representative test modules include [`test_clean.py`](../tests/test_clean.py), [`test_golden_tables.py`](../tests/test_golden_tables.py), [`test_scoring.py`](../tests/test_scoring.py), [`test_quality.py`](../tests/test_quality.py), [`test_pipeline.py`](../tests/test_pipeline.py) and [`test_numeric_finiteness.py`](../tests/test_numeric_finiteness.py). The GitHub Actions workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) compiles the code and runs the source-independent subset; it does not connect to Azure. See the [reproducibility guide](reproducibility.md) for exact commands and dependency setup.

A clean clone cannot reproduce the complete source-backed run without all four inputs and lawful access to them. AVI0301/ICAO source rights remain unresolved. No live Azure, Cognos, watsonx or Power BI service, scheduled refresh, current global ranking, retail profitability or causal/forecast result is claimed.
