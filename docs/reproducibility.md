# Reproducibility

## Inputs

The pipeline expects four CSVs in `data/raw/`, with exact paths in `src/airtraffic/config.py`. None are bundled. AVI0301 is ICAO-sourced; its raw CSV and canonical derived table outputs are not included. The owner explicitly authorizes publication of the original authored dashboard screenshots containing historical displays; those images are not current pipeline exports or independent validation. The CAA and DfT/DataSF source conditions are documented in [`data-sources-and-licensing.md`](data-sources-and-licensing.md). The public `source_manifest.json` records only source-relative paths, byte sizes and SHA-256 digests; it contains no sample rows. `outputs/qa/source_schema.txt`, which includes sample rows, is local-only.

## Environment and commands

Python >=3.11 is declared in `pyproject.toml`; dependency constraints and exact resolution are in `pyproject.toml` and `uv.lock`. Install from the committed lock with:

```bash
uv sync --locked --extra dev --python 3.11
```

Run the public source-independent checks:

```bash
uv run --locked python -m compileall -q src scripts tests
uv run --locked pytest -q -m "not requires_sources"
```

The complete local suite is `uv run --locked pytest -q` and requires all four locally obtained source CSVs under `data/raw/`. Public CI collects the suite but executes only the self-contained tests; source-dependent tests are reported as not run rather than passed or silently skipped. The CI policy and counts are documented in the [README](../README.md#continuous-integration).

With the locked package installed and all four lawful local inputs available, run a new local pipeline build with:

```bash
uv run --locked python -m airtraffic.pipeline
```

The pipeline reads the four local CSVs and writes a new run directory under `outputs/runs/`; it does not write to Azure. It may also refresh the latest convenience exports in `outputs/`, so preserve or back up local outputs before running it.

## Canonical archived run

The public evidence summary references run `20261005T163644Z_33f9f4ffa323`, recorded status `VALIDATED_LOCAL`, model version `BI_DECISION_V2.0.0`, and the check totals (30 checks, zero failures/warnings). Public copies of the source/artifact manifests contain paths, sizes and hashes only. During the local audit, the canonical manifests were checked against all listed source/output files; the data-bearing outputs themselves remain local-only. The summary intentionally omits per-table row counts, candidate identities and benchmark values.

Re-running the pipeline creates a new run ID and generated timestamp. The canonical ID is provenance for an archived run, not a deterministic expected ID. A reproducibility comparison should use identical source hashes, pipeline/model versions, output hashes, and QA results.

## Cloud boundary

`sql/schema.sql`, `sql/views.sql`, and `sql/validation_queries.sql` describe the SQL Server publication/validation contract. `scripts/validate_published_run.py` connects to a database and prompts for a password; `scripts/publish_validated_run.py` can modify a database. These commands were not run during this preparation because they require cloud access and may read/write external resources. Do not run the publisher without explicit operational approval.

Only the SQL contracts and code are published as executable artifacts. Historical Azure validation logs with data-bearing result rows remain local and were not rerun; the exact historic SQL screenshot is included separately in the authorized evidence gallery.

## Known limits

- AVI0301 raw input and canonical row-level outputs are not bundled; original owner-authorized screenshots may contain historical displayed values, without asserting current validation.
- The approved MIT `LICENSE` applies to original code only; third-party materials remain under their own terms.
- Coverage is not configured; no coverage figure is claimed.
- No Azure, Power BI, or Cognos live deployment was independently checked.
