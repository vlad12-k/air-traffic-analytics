# Architecture

## Current V2 analytical flow

```text
AVI0105 ─┐
AVI0301 ─┤
ROUTES ──┼─> Python source ingestion ─> cleaning / standardisation
SFO ─────┘                                  │
                                           v
                             governed GT1–GT8 contracts
                                           │
                                  explainable GT10 model
                                           │
                           quality checks / reconciliations
                                           │
                         GT9 + run metadata + local export
                                           │
                      Azure SQL publication design (T-SQL)
                                           │
                                    Power BI V2
```

The Python package is the current, locally testable transformation and validation implementation. SQL scripts define run-aware `meta`, `bi`, and `reporting` structures. Reporting views select the latest successfully published run; that is a database design, not evidence that a live Azure service currently exists.

Power BI V2 is the current report evidence layer. The screenshots establish what the report/model pages looked like when captured; they do not establish a currently accessible Power BI deployment or a live refresh.

## Historical implementation

IBM Cognos dashboards and semantic model, Google Colab upload workflow, Azure portal/SQL screenshots, and IBM watsonx/AutoAI work are preserved under `docs/evidence/historical/`. They are labelled historical and are not substitutes for current V2 pipeline execution evidence.

## Governed contract boundaries

- GT1–GT8: source-grounded market, comparison, connectivity, flow, and benchmark tables.
- GT9: per-run operational and data-quality KPIs.
- GT10: versioned recommendation rows separated by `UK_SITE` and `GLOBAL_EXPANSION`, with explicit scenarios and policy weights.
- Quality gates and reconciliation run before local export. Azure publication is a separate, credentialed operation.

For metric grain and assumptions, see [`gt-contracts.md`](gt-contracts.md), [`decision-model.md`](decision-model.md), and [`lineage.md`](lineage.md).
