# AirTrafficAnalytics

**Evidence-driven airport expansion decision intelligence** for two distinct decisions: UK airport site selection and later global airport expansion. The project uses public aviation sources, governed GT1–GT10 tables, reconciliation and explicit sensitivity scenarios. It is a historical-snapshot decision-support portfolio—not a live airline or airport system, commercial feasibility study, forecast, or investment recommendation.

## Business problem and objectives

The work evaluates which observed UK airport market could support opening the first boutique and which non-UK airport may merit later expansion review. It compares passenger demand and market position, period-on-period recovery context, destination/country connectivity, airport benchmarks, and candidate scenarios. Quality checks, source reconciliation, sensitivity to policy weights, and explicit data/model limitations support the decisions. UK and global candidate populations remain separate; scores are comparative indicators, not forecasts, causal claims, or proof of commercial viability.

The full methodology, KPI contracts, findings and limitations are documented in the [business case study](docs/business-case-study.md). A separate formal stakeholder matrix or original academic report was not located in this project folder.

## Current verified work

- Python V2 ingestion, cleaning, transformations, GT1–GT10 generation, quality checks, reconciliation, run metadata, and local validated-run export.
- SQL Server schema and reporting-view definitions for run-scoped analytical tables and validation queries.
- A canonical local run (`20261005T163644Z_33f9f4ffa323`) and its manifests/QA results, preserved locally. Only non-data provenance manifests and a source-free validation summary are in the public candidate; ICAO-derived tables and detailed QA remain local-only.
- Two unchanged, schema-only Microsoft Power BI screenshots (model/relationships) are included under published screenshot guidance; data-bearing report pages remain local-only.

The canonical run is an archived local validation result, not a claim that the pipeline was freshly run during release preparation. Detailed Azure validation logs and SQL result grids are retained locally because they include data-bearing recommendations; the public validation summary does not imply a currently running Azure service.

## Project and release scope

The complete original working project, source files and canonical run remain preserved locally. The Git candidate is a deliberately reduced, rights-filtered snapshot: raw datasets and AVI0301-derived outputs/screenshots are omitted, not reconstructed or substituted. Historical Cognos/Colab/Azure/watsonx materials stay labeled as historical; the current analytical implementation is the Python V2 package and the current report layer is Power BI V2 evidence.

## Architecture

```text
Public aviation source extracts
          ↓
Python ingestion, cleaning, transformation
          ↓
GT1–GT8 analytical contracts + GT10 decision model
          ↓
Quality gates, reconciliation, GT9 operational KPIs,
run metadata and validated local exports
          ↓
Azure SQL publication design (meta / bi / reporting)
          ↓
Power BI V2 reporting
```

The architecture and scope are described in [`docs/architecture.md`](docs/architecture.md); table definitions and model assumptions are documented in [`docs/gt-contracts.md`](docs/gt-contracts.md), [`docs/lineage.md`](docs/lineage.md), and [`docs/decision-model.md`](docs/decision-model.md).

## Data and provenance

The four local input datasets are identified by source IDs AVI0105, AVI0301, ROUTES and SFO. The public candidate does not bundle raw CSVs. The permitted source/artifact manifests contain only relative paths, hashes and sizes; sample schemas and data-bearing QA are local-only. See [`docs/data-sources-and-licensing.md`](docs/data-sources-and-licensing.md) for publishers, terms, attribution and file-level exclusions. AVI0301 is ICAO-sourced and its redistribution rights remain unresolved; related data-bearing outputs are excluded rather than altered.

## UK_SITE evidence snapshot

![Original CAA-based UK airport market snapshot](docs/evidence/visualizations/uk-airport-market-snapshot.svg)

The original visualization uses permitted GT3 data from the CAA May 2022 route snapshot, not a vendor screenshot. Within the 36-airport population represented in that extract, Heathrow leads passenger scale (4.99 million; 27.77%) and has the broadest observed network in GT8 (90 destination countries and 207 destination airports). In the canonical UK_SITE baseline, Heathrow ranks first and remains the leading candidate across the three UK weighting scenarios. This supports further due diligence—not a commercial opening decision. CAA attribution and the no-sale condition are printed in the chart. The full methods, findings and caveats are in the [business case study](docs/business-case-study.md).

## Governed tables and decision model

GT1–GT8 provide market, demand, connectivity, destination, and benchmark measures; GT9 records operational and data-quality KPIs; GT10 stores recommendations at candidate × decision scope × scenario × model version grain. Global expansion and UK-site rankings are computed independently. The project includes baseline and alternative policy-weight scenarios; sensitivity results test ranking stability rather than statistical confidence.

## Power BI V2 report

The public candidate includes two unchanged schema-only **Microsoft Power BI** screenshots. They contain no third-party data rows or identifiable person; attribution: **“Used with permission from Microsoft.”** Report-page screenshots containing aviation data are not included because screenshot permission for third-party content is not established. The local evidence inventory is documented in the [Power BI index](docs/evidence/power-bi-v2/README.md).

| Power BI semantic model | Power BI relationships |
|---|---|
| ![Microsoft Power BI semantic model overview](docs/evidence/power-bi-v2/powerbi-v2-08-semantic-model-overview.png) | ![Microsoft Power BI relationships overview](docs/evidence/power-bi-v2/powerbi-v2-09-relationships-overview.png) |

Used with permission from Microsoft. These schema-only screenshots are unchanged, contain no third-party data rows and are included under Microsoft's published screenshot guidance.

## Historical evidence

IBM Cognos, Colab-to-Azure, Azure SQL and watsonx captures are retained locally as historical evidence, not represented as current deployments. Vendor UI screenshots are excluded because product screenshot reuse permission is not documented; CAA/AVI0301 data-bearing images have the additional source-rights conditions described in the licensing file. The SIPOC original is also local-only pending authorship confirmation. Browse the indexes: [Cognos](docs/evidence/historical/cognos/README.md), [Colab](docs/evidence/historical/colab/README.md), [Azure](docs/evidence/historical/azure/README.md), [watsonx](docs/evidence/historical/watsonx/README.md), and [process](docs/evidence/historical/process/README.md).

## Validation and data quality

A public, source-free summary of the archived local validation is in [`docs/evidence/validation/README.md`](docs/evidence/validation/README.md). It reports the local run status and QA-check outcome but omits candidate rankings, source row counts, sample rows and data-bearing SQL results. Full QA, detailed run outputs and the Azure transcript remain local-only. The existing SQL validation query is documented code; it was not executed against Azure during this release preparation.

## Reproduce locally

1. Use Python 3.11 or newer and create an isolated environment.
2. Install the project and development test dependency from `pyproject.toml`/`uv.lock` (for example, `python -m pip install -e '.[dev]'`).
3. To use Azure-only scripts, copy `.env.example` to a private local file or export `AZURE_SQL_SERVER`, `AZURE_SQL_DATABASE`, and `AZURE_SQL_USERNAME` in the shell. The scripts ask for the password using masked input; `.env.example` is a template and is not loaded automatically. Never commit a real `.env` file.
4. Full end-to-end tests and pipeline run require all four locally obtained source CSVs at the paths in `src/airtraffic/config.py`. They are not bundled. Use only copies whose publisher terms permit your use; AVI0301 is ICAO-sourced and rights remain unresolved, so a clean-clone full run must wait for permission. The manifest in `docs/evidence/validation/` is a checksum inventory, not a copy of the data.
5. Run the tests: `python -m pytest -q`.
6. To build a new local run, use `python -m airtraffic.pipeline` with `src/` on `PYTHONPATH` (or install the project editable first). This writes a new run under `outputs/runs/`; it does not update Azure.

The test suite was rerun after the release-safety configuration change: **37 passed**. Re-running the pipeline creates a new timestamped run and is not expected to reproduce the canonical run ID; compare source hashes, output hashes, and the documented pipeline/model versions instead. Coverage is not configured.

## Limitations

- Inputs are historical snapshots, not a live feed. The UK route comparison covers the source-supplied period; it should not be described as a multi-year UK airport time series.
- The global airport benchmark is limited to the airports and years present in AVI0301; it does not establish profitability, route availability, or commercial feasibility.
- Scenario outputs are decision-support rankings based on explicit policy weights, not causal estimates, forecasts, or probabilities.
- The legacy root `main.py` contains unvalidated placeholder scoring assumptions and is retained locally but excluded from the public candidate; the V2 package under `src/airtraffic` is the canonical execution path.
- AVI0301-derived outputs and data-bearing screenshots remain excluded pending confirmation of ICAO/DfT redistribution rights.
- IBM Cognos/watsonx and Google Colab UI screenshots remain local-only because no screenshot-reuse permission was documented; the altered Azure capture is also withheld. Only unaltered, schema-only Microsoft Power BI screenshots are included under Microsoft’s published screenshot guidance.
- The MIT license covers only original project code; third-party datasets, screenshots and materials remain under their own terms.
- No live Azure SQL, Power BI, Cognos or watsonx deployment is claimed; screenshots are historical evidence.

## License

[`LICENSE`](LICENSE) applies the MIT License to original project code authored by Vladyslav Kononov. The owner approved this license. It does not apply to aviation datasets, derived source data, screenshots or other third-party materials; see [`docs/data-sources-and-licensing.md`](docs/data-sources-and-licensing.md).

## Technology

Python, pandas, NumPy, SciPy, pytest, CSV/XLSX, SQL Server/T-SQL, Azure SQL (historical evidence/publication target), and Power BI (V2 report evidence). IBM Cognos, Google Colab, and IBM watsonx/AutoAI are historical components.
