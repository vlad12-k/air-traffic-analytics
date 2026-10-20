# Analytical Lineage

## Core architecture

Public aviation sources
        |
        v
Ingestion and source profiling
        |
        v
Cleaning and standardisation
        |
        v
Feature engineering and reconciliation
        |
        v
Governed analytical contracts GT1–GT10
        |
        v
Azure SQL governed analytical store
        |
        +----------------------+
        |                      |
        v                      v
IBM Cognos Analytics       IBM watsonx / AutoAI
        |
        v
Executive / tactical / operational decision support

## V2 engineering assurance

The refactored implementation adds:

- package-based Python transformation logic
- schema contracts
- automated tests
- source-to-GT reconciliation
- explicit metric definitions
- decision-model versioning
- quality gates
- run metadata and manifests
- SQL validation query definitions

These are local engineering artifacts. No automated remote CI workflow was found during this preparation, and cloud operations are not invoked by the local test suite.

---

## Current and historical BI consumers

Power BI V2 is the current report-evidence layer for the governed GT contracts. Eleven report/model screenshots are retained under `docs/evidence/power-bi-v2/`; the screenshots do not prove a live published service or refresh schedule.

IBM Cognos is historical BI evidence and remains separate from the V2 report. Colab-to-Azure screenshots document the original workflow, not the current Python pipeline.

The Azure SQL schema/publication design is documented in `sql/`. It defines run-scoped governed tables and reporting views over the latest published run, but no active Azure deployment is claimed here.

For the concise current-state diagram and scope, see `docs/architecture.md`.
