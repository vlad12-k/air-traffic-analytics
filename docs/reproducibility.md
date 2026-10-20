# Reproducibility

## Inputs

The pipeline expects four CSVs in `data/raw/`, with exact paths in `src/airtraffic/config.py`. None are bundled. AVI0301 is ICAO-sourced with redistribution rights unresolved; do not include it or derived data in the public package until those rights are cleared. A lawful local copy may be used for private validation. The CAA and DfT/DataSF sources have attribution/conditions documented in [`data-sources-and-licensing.md`](data-sources-and-licensing.md). The public `source_manifest.json` records only source-relative paths, byte sizes and SHA-256 digests; it contains no sample rows. `outputs/qa/source_schema.txt`, which includes sample rows, is local-only.

## Environment and commands

Python >=3.11 is declared in `pyproject.toml`; dependency constraints and lock information are in `pyproject.toml` and `uv.lock`. Create an isolated environment and install the project plus its `dev` extra using your chosen package manager. Dependencies were not installed as part of the release-preparation work.

Run the automated tests:

```bash
python -m pytest -q
```

Run a new local analytical pipeline build after the editable package is installed:

```bash
python -m airtraffic.pipeline
```

Alternatively, set `PYTHONPATH=src` for the command. Pipeline execution reads the four local CSVs and writes a new run directory under `outputs/runs/`; it does not write to Azure. It may also refresh the latest convenience exports in `outputs/`, so preserve or back up any local outputs before a run.

## Canonical archived run

The public evidence summary references run `20261005T163644Z_33f9f4ffa323`, recorded status `VALIDATED_LOCAL`, model version `BI_DECISION_V2.0.0`, and the check totals (30 checks, zero failures/warnings). Public copies of the source/artifact manifests contain paths, sizes and hashes only. During the local audit, the canonical manifests were checked against all listed source/output files; the data-bearing outputs themselves remain local-only. The summary intentionally omits per-table row counts, candidate identities and benchmark values.

Re-running the pipeline creates a new run ID and generated timestamp. The canonical ID is provenance for an archived run, not a deterministic expected ID. A reproducibility comparison should use identical source hashes, pipeline/model versions, output hashes, and QA results.

## Cloud boundary

`sql/schema.sql`, `sql/views.sql`, and `sql/validation_queries.sql` describe the SQL Server publication/validation contract. `scripts/validate_published_run.py` connects to a database and prompts for a password; `scripts/publish_validated_run.py` can modify a database. These commands were not run during this preparation because they require cloud access and may read/write external resources. Do not run the publisher without explicit operational approval.

Only the SQL contracts and code are public-candidate files. Historical Azure validation logs contain data-bearing result rows, remain local-only, and were not rerun.

## Known limits

- AVI0301/ICAO redistribution rights are unresolved; all affected outputs/screenshots remain local-only.
- The approved MIT `LICENSE` applies to original code only; third-party materials remain under their own terms.
- Coverage is not configured; no coverage figure is claimed.
- No Azure, Power BI, or Cognos live deployment was independently checked.
