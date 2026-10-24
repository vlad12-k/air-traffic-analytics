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
| AVI0301 | `data/raw/AVI0301.csv` | Global airport benchmark and GLOBAL_EXPANSION features | DfT notes identify ICAO lineage; raw source rows are not bundled. Original owner-authorized screenshots may show historical derived results; they are not reproduced as current analytical findings in prose. |
| ROUTES | `data/raw/Table_12_1_Intl_Air_Pax_Traffic_Route_Analysis.csv` | CAA UK airport demand, destination flow and connectivity snapshot | Not bundled; cite CAA Table 12.1, May 2022, and observe its no-sale condition. |
| SFO | `data/raw/Air_Traffic_Passenger_Statistics_2005-2020.csv` | External historical disruption benchmark | Not bundled; source provenance/terms are documented. |

[`ingest.py`](../src/airtraffic/ingest.py) reads those local inputs; it does not download them. [`scripts/inspect_sources.py`](../scripts/inspect_sources.py) profiles row/column counts, types, nulls, duplicates, and sample rows. That command can print restricted source rows and is for lawful local use only. Source URLs and terms are summarized in [data sources and licensing](data-sources-and-licensing.md).

**Inputs → outputs:** local source CSVs → in-memory source frames; the run context later records source-manifest metadata. No raw dataset is committed. The original screenshot archive and per-image status are listed in the [evidence index](evidence/README.md).

## 3. Inspection, cleaning and ETL

[`clean.py`](../src/airtraffic/clean.py) implements source-specific transformations rather than treating unlike sources as one table:

- AVI0105's country/year-wide layout is reshaped to long country/year rows; passenger-thousands are converted to passenger counts.
- AVI0301's airport benchmark labels and thousands units are normalized in code. Raw source rows are not bundled; selected historical derived values remain visible in the original owner-authorized screenshots and are not independently revalidated here.
- SFO empty `Unnamed:` columns are removed, dates parsed, and passenger counts typed.
- CAA ROUTES fields are renamed and normalized; the source period is parsed, current and prior passenger components retained, and growth is left null for a zero prior denominator. The snapshot is not represented as an annual airport history.

`tests/test_clean.py` contains source-dependent checks and a synthetic AVI0301 unit example. The exact original Colab screenshot and a separately labeled redacted derivative are both included in the [historical gallery](evidence/historical/README.md); the derivative masks the entire upload-result block but does not replace the original. No original `.ipynb` notebook is in the project tree. The V2 Python functions below are the current implementation; they are not claimed to be the historical Colab notebook code.

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
| GT7 | Global airport benchmark | AVI0301; historical report screenshots show earlier results; raw rows are not bundled |
| GT8 | UK destination breadth and scheduled/charter composition | CAA ROUTES |
| GT9 | Run-level operational, coverage and data-quality KPIs | Quality report and governed tables |
| GT10 | Candidate recommendations by scope, scenario and model version | Separate UK_SITE and GLOBAL_EXPANSION inputs/populations |

UK_SITE scores passenger scale, destination-country breadth, and destination-airport breadth using within-scope percentiles. GT2 growth is contextual because low or zero prior denominators can inflate ratios. GLOBAL_EXPANSION uses its own candidate population and features; scores are not compared across scopes. Historical global screenshot values are shown as archive evidence only; raw source rows are not published and no current global recommendation is claimed. Scenario weights are explicit policy parameters, not probabilities. See [`decision-model.md`](decision-model.md), [`gt-contracts.md`](gt-contracts.md), and [`lineage.md`](lineage.md).

Validation and reconciliation occur before local export. [`pipeline.py`](../src/airtraffic/pipeline.py) calls `assert_publishable()` before creating the operational layer and export artifacts. [`provenance.py`](../src/airtraffic/provenance.py) and [`export.py`](../src/airtraffic/export.py) attach run IDs and manifests.

## 5. Historical IBM Cognos Analytics

The project owner states that they created the Cognos reports and semantic model. Three authentic screenshots are included at the owner's direction:

- [Semantic model](evidence/historical/cognos/historical-cognos-07-semantic-model.png) — schema/model metadata, not result rows.
- [UK demand filter](evidence/historical/cognos/historical-cognos-11-demand-filter.png) — a filtered UK airport demand report using CAA-derived measures.
- [UK demand recovery](evidence/historical/cognos/historical-cognos-10-demand-recovery-original.png) — original two-period UK airport comparison; all ten displayed passenger pairs match the preserved GT1 output derived from CAA Table 12.1 (period 202205).

The complete set of eight original Cognos screenshots appears in the [Cognos technical gallery](evidence/historical/cognos/technical-notes.md). CAA source reference/no-resale conditions are retained on applicable UK pages; historical global/operational score lineage and the original Cognos queries, joins and refresh history are not fully reconstructable. Matching passenger totals do not validate other Cognos calculations. No Cognos package, query definitions or runnable source data are part of this repository. Image-level limitations and the owner's publication authorization are recorded in the [evidence index](evidence/README.md).

## 6. Historical Google Colab ETL

The [historical engineering evidence gallery](evidence/historical/README.md) displays all seven exact original archive PNGs; one authentic Colab derivative is shown separately with its entire data-bearing upload-result block masked.

![Historical Colab notebook with upload outputs redacted](evidence/historical/colab/colab-etl-upload-redacted.png)

The original screenshot evidences a historical notebook-based CSV-to-Azure-SQL handoff. The visible code uses a SQLAlchemy/ODBC connection, reads CSVs from `out/golden` and calls `DataFrame.to_sql(..., if_exists='replace')`; a connection-success message is visible. The image displays its historic upload output; a separate redacted derivative masks that area. The screenshot does not show a data-quality gate, source-target reconciliation, transaction-safe swap, notebook artifact or business finding. `if_exists='replace'` also means a rerun replaces destination tables; this is historical evidence, not a recommended current loading pattern or a current scheduled pipeline. The V2 ingestion/cleaning links above are the current code path, not a reconstruction of the notebook.

## 7. Historical Azure SQL storage and validation

The historical Azure screenshots show a resource/database view and a SQL validation result screen. Both exact originals appear in the [historical gallery](evidence/historical/README.md) under the owner's explicit authorization. They are historical evidence only; the grid is not independent validation and no live Azure resource was accessed or changed.

The current repository's Azure SQL layer is a deployable design, not an active service:

- [`sql/schema.sql`](../sql/schema.sql) defines run-aware `meta`, `bi`, and `reporting` schemas and audit structures.
- [`sql/views.sql`](../sql/views.sql) defines reporting views over the latest `PUBLISHED` run.
- [`sql/validation_queries.sql`](../sql/validation_queries.sql) contains independent post-publication reconciliation queries.
- [`scripts/apply_schema.py`](../scripts/apply_schema.py) and [`scripts/apply_views.py`](../scripts/apply_views.py) deploy schema/views; [`scripts/validate_published_run.py`](../scripts/validate_published_run.py) reads SQL results; [`scripts/publish_validated_run.py`](../scripts/publish_validated_run.py) can write a validated local run to the database.

Those database scripts require credentials or can affect external resources; no Azure operation was executed for this portfolio. The CI workflow does not connect to Azure. Its Azure-related unit tests validate connection-string construction only.

## 8. Historical IBM watsonx / AutoAI

The archive includes all three watsonx import/experiment screenshots (`05-watsonx-import.png`, `06-watsonx-autoai.png`, `10. Auto Ai experiment.png`); the exact originals appear in the [historical gallery](evidence/historical/README.md). The repository contains no AutoAI model or experiment export to replay; the available evidence is screenshot-based, not an independently rerun experiment. See the [evidence index](evidence/README.md).

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

The [Power BI technical gallery](evidence/power-bi-v2/technical-notes.md) contains all 11 exact original archive screenshots. SHA-256 verification confirms each included original matches its archive entry byte-for-byte. CAA attribution/no-resale conditions are preserved where relevant. No `.pbix`, `.pbit`, PDF export, live service, or refresh source is present/claimed. The gallery explains each page's visible measures, documented GT lineage, decision use, and validation/limitations boundary.

## 11. Business conclusion and limitations

The locally validated UK_SITE baseline identifies Heathrow as the lead within the represented CAA population and remains stable across the three documented UK policy scenarios. This is a priority for further site diligence, not proof of retail footfall or profitability. The project omits commercial decision inputs such as rent, retail conversion, available premises, category competition and operating margin. GLOBAL_EXPANSION is implemented as a distinct scope; historical global dashboard values appear in the owner-authorized original screenshots, but are not presented as current or independently revalidated findings.

## 12. Test and reproduction boundary

The complete local suite contains 45 tests. CI runs 11 self-contained tests; 34 `requires_sources` tests are collected but not run publicly because they need four local CSV inputs, including AVI0301. The CI job compiles code and checks locked dependencies; it makes no Azure connection and produces no data artifacts. For exact commands and scope see the [README CI section](../README.md#continuous-integration).

A clean clone cannot reproduce the source-backed full pipeline without the four locally obtained CSV inputs. The [evidence index](evidence/README.md) accounts for all 26 exact original PNGs (11 Power BI, eight Cognos, seven historical engineering/process images), plus one separate redacted Colab derivative. The four SVG visuals are supplementary and are not counted as platform screenshots.
