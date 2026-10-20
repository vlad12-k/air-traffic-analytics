# Public validation evidence

- [Source-free archived-run summary](release-validation-summary.md)
- [Source manifest](source_manifest.json) — relative paths, byte sizes and SHA-256 hashes only.
- [Artifact manifest](artifact_manifest.json) — paths, byte sizes and SHA-256 hashes only; some referenced outputs are intentionally absent from the public candidate.

The manifests contain no source rows, candidate names or traffic metrics. Their hashes do not grant redistribution permission for the referenced data.

## Local-only validation materials

The canonical run and original QA remain unchanged on disk. The following are excluded by `.gitignore` because they contain data-bearing AVI0301-derived values, source samples, detailed scores or SQL rows:

- `run_metadata.json` (per-table counts)
- `source_schema.txt` (sample rows)
- `quality_report.csv`
- `gt10_eligibility_report.csv`
- `gt10_sensitivity_summary.csv`
- `pipeline_run.txt`
- `azure_validation.txt`
- all files under `outputs/runs/`

The archived Azure transcript was not rerun. No Azure resource was accessed or modified. Local tests are reported separately from cloud validation.
