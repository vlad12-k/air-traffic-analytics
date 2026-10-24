# Historical engineering screenshots — full technical notes

This document covers all seven historical originals in archive order. All seven original PNGs appear in the gallery under the owner's latest explicit authorization. The Colab page also retains a separately counted redacted derivative for comparison; no raw CSVs are included. Current source-dependent code and tests are described as related implementation, not as historical validation.

## 1. SIPOC — process design

![Original SIPOC for airport site selection and prioritisation](process/01-business-process-sipoc.png)

**Business problem.** Turn an airport expansion question into a staged process that makes inputs, engineering steps, outputs and decision users explicit.

**Actual evidence.** The owner-authored diagram names CSV/ODS and API extracts plus a schema dictionary; source profiling; cleaning/harmonisation; feature engineering for year-on-year change, recovery, share and routes; publishing GT1–GT10; dashboard/AutoAI insight composition; and decision-pack review. It lists golden tables, KPI/ranked-list outputs, a data dictionary and change log, with executive, store-operations and delivery audiences.

**Model and implementation link.** The current Python pipeline implements local-file ingest, source-specific cleaning, GT1–GT8 construction, GT10 scoring, publication quality checks and run manifests. See [`ingest.py`](../../../src/airtraffic/ingest.py), [`clean.py`](../../../src/airtraffic/clean.py), [`golden.py`](../../../src/airtraffic/golden.py), [`scoring.py`](../../../src/airtraffic/scoring.py), [`quality.py`](../../../src/airtraffic/quality.py), [`pipeline.py`](../../../src/airtraffic/pipeline.py), and the [GT1–GT10 contracts](../../gt-contracts.md). Those artifacts are a current executable implementation related to the documented business problem; they do not prove that every historical SIPOC hand-off occurred.

**Decision and validation limit.** The diagram defines an intended decision workflow, not the answer to a site-selection question. It does not establish that the sources, transformations, dashboards or AutoAI experiments in the picture were all run together. The current test suite validates current code only. The original PNG is included unchanged after the owner's explicit authorship and publication confirmation.

## 2. Azure SQL — historical resource view

![Original Azure SQL resource/database screenshot](azure/historical-azure-sql-database-original.png)

**Business purpose.** Record the earlier relational-storage target used for the golden-table hand-off, with resource status, capacity/storage and operational-navigation context.

**What is visible.** OCR of the original identifies a database/resource view and reveals subscription, resource-group, server, account and connection-context identifiers. These remain visible in the original screenshot and are not separately transcribed into the prose. No raw aviation rows are visible; the owner has expressly authorized publication of this screenshot despite the resource metadata. No password or access token is intentionally published.

**Implementation and model connection.** The current, separate SQL publication design lives in [`sql/schema.sql`](../../../sql/schema.sql), [`sql/views.sql`](../../../sql/views.sql), and [`sql/validation_queries.sql`](../../../sql/validation_queries.sql); deployment helpers are in [`scripts/apply_schema.py`](../../../scripts/apply_schema.py), [`scripts/apply_views.py`](../../../scripts/apply_views.py), and [`scripts/publish_validated_run.py`](../../../scripts/publish_validated_run.py). The screenshot does not prove that the current schema was deployed to the historical resource or that the resource still exists. No Azure account/resource was accessed during this task.

**Publication boundary.** The original is included under the owner's latest explicit authorization. It visibly contains Azure account/resource identifiers; no separate password or token is transcribed into the repository. Microsoft UI is visible, with no endorsement or bespoke permission claimed.

## 3. Google Colab — CSV-to-Azure SQL hand-off

![Original Google Colab ETL screenshot from the archive](colab/colab-etl-upload-original.png)

![Authentic Colab screenshot with the data-bearing upload-output block masked](colab/colab-etl-upload-redacted.png)

**Business problem.** Make curated CSV tables available to later SQL/BI tooling through a historical notebook workflow.

**Implementation visible in the original.** The screenshot shows a SQLAlchemy/ODBC connection string assembled from variables, ODBC Driver 18 with encryption enabled and certificate trust disabled, iteration over `out/golden`, `pandas.read_csv`, and `DataFrame.to_sql(..., if_exists='replace', index=False)`. The displayed success message indicates a connection was established in that captured session. `replace` semantics overwrite destination tables on rerun; the screenshot does not show a transactional staging/swap, rollback, schema-contract check, reconciliation or run manifest. The notebook source and execution metadata are not in the repository.

**Data and publication boundary.** The original output block names tables and includes AVI0301/GT7-derived and mixed-source counts. The owner authorizes publication of the original screenshot; raw CSVs remain excluded. The derivative masks the complete output region, preserves the original pixels elsewhere, and is counted separately. It is not a substitute implementation or proof that any current V2 transformation ran in Colab. The related current code is [`ingest.py`](../../../src/airtraffic/ingest.py) and [`pipeline.py`](../../../src/airtraffic/pipeline.py); that code is not claimed to reproduce the historic notebook line-for-line.

## 4. Azure SQL — historical validation result grid

![Original Azure SQL validation query/results screenshot](azure/historical-azure-sql-validation-original.png)

**Business purpose.** Show a historical query-editor state and a populated recommendation-result grid after the earlier table upload.

**What is visible.** The screen includes a GT1–GT10-style object list and populated recommendation fields such as airport, passenger total, route count, recovery and composite score. The captured query text is not legible as an exported query, and the result includes global/candidate values plus account context. Numeric values and candidate rows are not repeated here.

**Model and SQL boundary.** The current SQL equivalent is separately documented in [`sql/schema.sql`](../../../sql/schema.sql), [`sql/views.sql`](../../../sql/views.sql) and [`sql/validation_queries.sql`](../../../sql/validation_queries.sql). Current QA/reconciliation is implemented in [`quality.py`](../../../src/airtraffic/quality.py) and tested in [`test_quality.py`](../../../tests/test_quality.py). These files are not asserted to be the historical query shown in the screenshot. The screen alone proves neither successful source-to-target reconciliation nor a trustworthy recommendation; there is no retained query export, source snapshot, run identity or comparison report linked to it.

**Publication boundary.** The original is included under the owner's explicit direction. It shows source-dependent recommendation values and account context; the image is historical evidence, not independently validated output or a current Microsoft/Azure deployment.

## 5. IBM watsonx — asset import

![Original IBM watsonx import/assets screenshot](watsonx/historical-watsonx-import-original.png)

**Business purpose.** Bring the earlier golden-table assets from the Azure SQL connection into the named watsonx project for subsequent experiment exploration.

**What is visible.** The capture shows the connected-data/asset-picker flow and a selection containing ten GT-named assets. This evidences an import-selection workflow only. It does not prove that every asset loaded successfully, that the imported schema matched current GT contracts, or that any model trained or passed validation.

**Model connection and limits.** GT1–GT10 names are also documented in the current model contracts, but the archive contains no watsonx import manifest, project export, SQL snapshot, training notebook or model artifact that links the import to the current V2 pipeline. The screenshot shows an account label and source context; these are not separately transcribed in the prose. No actual watsonx service or project was accessed or changed.

**Publication boundary.** The original is included under the owner's explicit authorization. Account/source labels and IBM UI are visible; no IBM endorsement or bespoke IBM permission is claimed.

## 6. IBM watsonx AutoAI — experiment overview

![Original IBM watsonx AutoAI experiment overview](watsonx/historical-watsonx-autoai-original.png)

**Business question.** Explore whether the historical passenger-traffic target could be modelled from the available route-analysis features and compare generated pipelines.

**What the screenshot evidences.** The AutoAI experiment screen displays a truncated passenger-traffic target, a generated pipeline leaderboard with Ridge and Linear Regression entries, and evaluation fields for cross-validation/holdout error and R². Several displayed fit metrics are near-perfect. This is a prompt for validation, not a defensible accuracy claim: a near-perfect score can arise from leakage, target-derived features, small/duplicate splits or evaluation setup. The screenshot alone cannot determine which explanation applies.

**Required validation not evidenced.** The experiment export, feature list, train/test row identities, leakage audit, time-aware holdout, baseline, residual analysis, reproducible training code and independent test results are absent. No forecasting result or production model is claimed. The CAA source attribution/no-sale condition remains relevant to source-derived metrics. The original is included at the owner's direction; the screenshot does not establish model validity or IBM endorsement.

**Current-code separation.** The current airport-site decision model is deterministic scoring in [`scoring.py`](../../../src/airtraffic/scoring.py), not this historical AutoAI training experiment. Current GT tables and tests do not validate AutoAI performance.

## 7. IBM watsonx AutoAI — pipeline comparison detail

![Original IBM watsonx AutoAI pipeline comparison](watsonx/historical-watsonx-10-autoai-experiment-original.png)

**Purpose.** Provide a second view of generated pipeline candidates and their comparative evaluation, including leaderboard, metrics, feature-engineering/optimisation indicators and build-time context.

**Interpretation.** The image documents that an AutoAI comparison was displayed in the captured session. It does not provide the exported model, exact target/source table snapshot, feature definitions, split design or code needed to rerun and explain the leaderboard. The displayed fit statistics are not presented as business outcomes or generalisation evidence. No independent model comparison, deployment or business decision is evidenced.

**Publication and lineage boundary.** The original contains IBM UI, account context and CAA-derived experiment metrics; it is included at the owner's explicit direction, without a claim of IBM endorsement. The current repository's tests and the recorded local quality run cover Python/SQL V2, not this AutoAI experiment.

## Cross-project evidence boundaries

- **Source rights:** the owner explicitly represents that the screenshot publication is cleared. DfT notes identify AVI0301 as ICAO-supplied; CAA Table 12.1 attribution and no-sale/no-resale conditions remain documented. Raw CSVs and canonical source outputs are not included. See [data-source terms](../../data-sources-and-licensing.md).
- **Current code/SQL:** the code links above are real current project files, not reconstructed historical files. Run-aware SQL tables, views and validation queries do not prove the historic Azure resource or Colab load used them.
- **Tests:** the project records 45 local tests; 34 require local source data, while the public-safe 11-test subset runs in CI. No historical screenshot is validated by those test counts.
- **Claims:** these images document stages and screens, not a current Azure service, scheduled pipeline, deployed Cognos report, deployed AutoAI model, live Power BI service, forecast quality or commercial result.

The [historical gallery](README.md), [Power BI technical notes](../power-bi-v2/technical-notes.md), [Cognos technical notes](cognos/technical-notes.md), and [full archive inventory](../README.md) keep each image linked to its project stage and publication boundary.
