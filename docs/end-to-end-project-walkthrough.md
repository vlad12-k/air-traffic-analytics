# AirTrafficAnalytics — end-to-end project walkthrough

This walkthrough maps the original boutique-retail airport expansion question to the historical BI work and the current Python/SQL V2 package. It distinguishes screenshot evidence from executable code and from cloud resources. Historical tools are not presented as current deployments, and no direct technical migration from Cognos to Power BI is claimed.

**Short flow:** business decisions → locally obtained aviation extracts → source profiling and cleaning → governed GT1–GT10 model and reconciliation → historical Cognos reporting → historical Colab ETL and Azure SQL validation → historical watsonx/AutoAI exploration → current Python/SQL V2 → Power BI V2 → sensitivity-based UK_SITE decision support.

## 1. Business problem and decisions

The business concept is a boutique retailer considering airport markets for a first UK store and later international expansion. The two decisions are kept separate:

- **UK_SITE:** Which represented UK airport should receive further site diligence for the first boutique?
- **GLOBAL_EXPANSION:** Which non-UK airports warrant later investigation?

The model supports screening, not a lease decision, sales forecast, profitability claim, or investment recommendation. Retail footfall, available premises, rent, category competition, conversion, basket size, operating costs, and unit economics are not in this analysis. The intended decision owner is inferred from the business question; the repository has no formal stakeholder matrix or original requirements deck.

**Evidence and method:** [business case study](business-case-study.md), [decision model](decision-model.md), [GT contracts](gt-contracts.md).

## 2. Data acquisition and source boundary

The project owner reports that the college provided source links and learning resources. The current package reads four local CSVs configured in [`src/airtraffic/config.py`](../src/airtraffic/config.py):

| Source ID | Source file (local input path) | Purpose in this project | Public boundary |
|---|---|---|---|
| AVI0105 | `data/raw/AVI0105.csv` | Country-level UK international passenger context | Not bundled; source/table conditions apply. |
| AVI0301 | `data/raw/AVI0301.csv` | Global airport benchmark and GLOBAL_EXPANSION features | DfT notes identify ICAO lineage; redistribution basis remains unresolved, so source rows and dependent global results stay local. |
| ROUTES | `data/raw/Table_12_1_Intl_Air_Pax_Traffic_Route_Analysis.csv` | CAA UK airport demand, destination flow and connectivity snapshot | Not bundled; cite CAA Table 12.1, May 2022, and observe its no-sale condition. |
| SFO | `data/raw/Air_Traffic_Passenger_Statistics_2005-2020.csv` | External historical disruption benchmark | Not bundled; source provenance/terms are documented. |

[`ingest.py`](../src/airtraffic/ingest.py) reads those local inputs; it does not download them. [`scripts/inspect_sources.py`](../scripts/inspect_sources.py) profiles row/column counts, types, nulls, duplicates, and sample rows. That command can print restricted source rows and is for lawful local use only. Source URLs and terms are summarized in [data sources and licensing](data-sources-and-licensing.md).

**Inputs → outputs:** local source CSVs → in-memory source frames; the run context later records source-manifest metadata. No raw dataset is committed. The original screenshot archive and per-image status are listed in the [evidence index](evidence/README.md).

## 3. Inspection, cleaning and ETL

[`clean.py`](../src/airtraffic/clean.py) implements source-specific transformations rather than treating unlike sources as one table:

- AVI0105's country/year-wide layout is reshaped to long country/year rows; passenger-thousands are converted to passenger counts.
- AVI0301's airport benchmark labels and thousands units are normalized in code, but AVI0301-derived outputs remain local under the existing rights restriction.
- SFO empty `Unnamed:` columns are removed, dates parsed, and passenger counts typed.
- CAA ROUTES fields are renamed and normalized; the source period is parsed, current and prior passenger components retained, and growth is left null for a zero prior denominator. The snapshot is not represented as an annual airport history.

`tests/test_clean.py` contains both source-dependent checks and a synthetic AVI0301 unit example. The original Colab screenshot `03-colab-azure-etl.png` is local-only because its upload log includes AVI0301-linked counts and Google UI/account context. No original `.ipynb` notebook is in the project tree. The V2 Python functions below are the current implementation; they are not claimed to be the historical Colab notebook code.

## 4. Governed measures, scoring and quality gates

[`golden.py`](../src/airtraffic/golden.py) constructs GT1–GT8; [`scoring.py`](../src/airtraffic/scoring.py) builds eligibility and GT10 decision records; [`quality.py`](../src/airtraffic/quality.py) evaluates reconciliations and gates publication.

| Contract | Actual responsibility | Primary lineage |
|---|---|---|
| GT1 | Current/prior passenger totals per UK airport | CAA ROUTES |
| GT2 | UK period change with zero-baseline context | GT1 / CAA ROUTES |
| GT3 | Ranking the full represented UK airport population | GT1 |
| GT4 | UK airport × destination-country passenger flow | CAA ROUTES |
| GT5 | Country-level passenger trend context | AVI0105 |
| GT6 | SFO historical benchmark | SFO/DataSF |
| GT7 | Global airport benchmark | AVI0301; the results are not public |
| GT8 | UK destination breadth and scheduled/charter composition | CAA ROUTES |
| GT9 | Run-level operational, coverage and data-quality KPIs | Quality report and governed tables |
| GT10 | Candidate recommendations by scope, scenario and model version | Separate UK_SITE and restricted GLOBAL_EXPANSION inputs |

UK_SITE scores passenger scale, destination-country breadth, and destination-airport breadth using within-scope percentiles. GT2 growth is contextual because low or zero prior denominators can inflate ratios. GLOBAL_EXPANSION uses its own candidate population and features; scores are not compared across scopes and global candidate outputs remain withheld. Scenario weights are explicit policy parameters, not probabilities. See [`decision-model.md`](decision-model.md), [`gt-contracts.md`](gt-contracts.md), and [`lineage.md`](lineage.md).

Validation and reconciliation occur before local export. [`pipeline.py`](../src/airtraffic/pipeline.py) calls `assert_publishable()` before creating the operational layer and export artifacts. [`provenance.py`](../src/airtraffic/provenance.py) and [`export.py`](../src/airtraffic/export.py) attach run IDs and manifests.

## 5. Historical IBM Cognos Analytics

The project owner states that they created the Cognos reports and semantic model. Two authentic screenshots are included at the owner's direction:

- [Semantic model](evidence/historical/cognos/historical-cognos-07-semantic-model.png) — schema/model metadata, not result rows.
- [UK demand filter](evidence/historical/cognos/historical-cognos-11-demand-filter.png) — a filtered UK airport demand report using CAA-derived measures.

The captures show IBM Cognos UI; no IBM permission or endorsement is claimed. CAA source reference and no-resale conditions apply to the demand page. The other Cognos images remain local: the recovery page's global comparison has no source lineage visible in the screenshot; executive/global and operations/risk pages retain the existing AVI0301/ICAO restriction. No original Cognos report package/PDF export is in the project tree, so no UI-free export could be prepared from these files. Exact filenames and local-only reasons are in [evidence/README.md](evidence/README.md).

## 6. Historical Google Colab ETL

The archived `03-colab-azure-etl.png` documents a notebook-based upload workflow that connected data preparation to Azure SQL. It is not public: the original screen contains AVI0301-linked output counts and Google account/UI context, and there is no notebook file to inspect or replay. The evidence shows a historical workflow, not a current scheduled pipeline. The V2 ingestion/cleaning links above are the current code path, not a reconstruction of the Colab notebook.

## 7. Historical Azure SQL storage and validation

The historical Azure screenshots show a resource/database view and a SQL validation result screen. They remain local: the original resource image exposes infrastructure identifiers, and the validation grid displays data-bearing recommendation/global results. The local redacted copies are not substituted for the originals in the public gallery.

The current repository's Azure SQL layer is a deployable design, not an active service:

- [`sql/schema.sql`](../sql/schema.sql) defines run-aware `meta`, `bi`, and `reporting` schemas and audit structures.
- [`sql/views.sql`](../sql/views.sql) defines reporting views over the latest `PUBLISHED` run.
- [`sql/validation_queries.sql`](../sql/validation_queries.sql) contains independent post-publication reconciliation queries.
- [`scripts/apply_schema.py`](../scripts/apply_schema.py) and [`scripts/apply_views.py`](../scripts/apply_views.py) deploy schema/views; [`scripts/validate_published_run.py`](../scripts/validate_published_run.py) reads SQL results; [`scripts/publish_validated_run.py`](../scripts/publish_validated_run.py) can write a validated local run to the database.

Those database scripts require credentials or can affect external resources; no Azure operation was executed for this portfolio. The CI workflow does not connect to Azure. Its Azure-related unit tests validate connection-string construction only.

## 8. Historical IBM watsonx / AutoAI

The archive includes import/experiment screenshots (`05-watsonx-import.png`, `06-watsonx-autoai.png`, `10. Auto Ai experiment.png`). They remain local because the captures contain IBM UI and account/source context, and the AutoAI images include CAA-derived metrics. The repository contains no AutoAI model or experiment export to replay; the available evidence is screenshot-based, not an independently rerun experiment. See the [evidence index](evidence/README.md).

## 9. Current Python/SQL V2 pipeline

The implemented local execution path in [`pipeline.py`](../src/airtraffic/pipeline.py) is:

1. Load the four configured local sources.
2. Clean and standardize each source.
3. Build GT1–GT8 and the GT10 recommendation model.
4. Reconcile counts/components and evaluate quality checks.
5. Stop if the publication gate detects an error-level failure.
6. Build GT9, add run IDs, sensitivity and eligibility summaries.
7. Export a run-specific local directory containing golden tables, QA reports, and metadata/manifests.

The canonical run recorded in the repository is `20261005T163644Z_33f9f4ffa323`, status `VALIDATED_LOCAL`, with 30 quality checks, zero failures and zero warnings. This is a recorded local run, not a run regenerated during this walkthrough. See the [release validation summary](evidence/validation/release-validation-summary.md), [`publish_validated_run.py`](../scripts/publish_validated_run.py), and [reproducibility notes](reproducibility.md). The public manifest copies contain path/size/hash metadata only; data-bearing canonical outputs remain local.

## 10. Current Microsoft Power BI V2 reporting

The report pages were personally authored by the project owner. Three original CAA-based captures are in the public gallery:

- [UK demand](evidence/power-bi-v2/powerbi-v2-02-uk-market-demand.png) — compares current/prior route passenger demand for UK_SITE screening.
- [UK_SITE sensitivity](evidence/power-bi-v2/powerbi-v2-05b-scenario-sensitivity-uk.png) — compares baseline, volume-heavy and connectivity-heavy policy scenarios.
- [Heathrow candidate detail](evidence/power-bi-v2/powerbi-v2-07b-candidate-detail-heathrow.png) — shows the candidate measures behind further site diligence.

The existing [semantic model](evidence/power-bi-v2/powerbi-v2-08-semantic-model-overview.png) and [relationships](evidence/power-bi-v2/powerbi-v2-09-relationships-overview.png) screenshots document the model layer. The five original captures were checked byte-for-byte against the named ZIP entries. The owner authorizes inclusion of their work; this does not assert Microsoft permission or endorsement. CAA attribution/no-resale conditions are preserved. The six other report pages—executive summary, destination connectivity, global benchmark/scenario, governance and Dubai candidate detail—remain local for the blockers in the [26-image inventory](evidence/README.md). No `.pbix`, `.pbit`, PDF export, live service, or refresh source is present/claimed.

## 11. Business conclusion and limitations

The locally validated UK_SITE baseline identifies Heathrow as the lead within the represented CAA population and remains stable across the three documented UK policy scenarios. This is a priority for further site diligence, not proof of retail footfall or profitability. The project omits commercial decision inputs such as rent, retail conversion, available premises, category competition and operating margin. GLOBAL_EXPANSION is implemented as a distinct scope but its names, ranks and scores are withheld while AVI0301/ICAO redistribution rights remain unresolved.

## 12. Test and reproduction boundary

The complete local suite contains 45 tests. CI runs 11 self-contained tests; 34 `requires_sources` tests are collected but not run publicly because they need four local CSV inputs, including AVI0301. The CI job compiles code and checks locked dependencies; it makes no Azure connection and produces no data artifacts. For exact commands and scope see the [README CI section](../README.md#continuous-integration).

A clean clone cannot reproduce the source-backed full pipeline until lawful local input access and AVI0301 rights are resolved. The [evidence index](evidence/README.md) accounts for all 26 original PNGs: seven are public (including two previously published schema images) and 19 remain local with item-specific reasons. The four SVG visuals are supplementary and are not counted as BI platform screenshots.
