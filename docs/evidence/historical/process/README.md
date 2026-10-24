# Historical process evidence — SIPOC

![Original SIPOC diagram for airport site selection and prioritisation](01-business-process-sipoc.png)

This is the **original archive PNG**, byte-identical to `Data GitHub Project/Cognos, Colab, Azure/01-business-process-sipoc.png`. The project owner has confirmed authorship and authorized publication. It is a process-design artifact, not a platform screenshot and not proof that every depicted step was executed.

## Business problem and intended workflow

The diagram frames the original airport-site question as a repeatable decision-support process rather than an informal ranking. It identifies CSV/ODS and API exports plus a schema dictionary as inputs; names the executive, store-operations, and delivery audiences; and outlines six stages:

1. Ingest and profile source extracts.
2. Clean and harmonise heterogeneous source structures.
3. Engineer year-over-year, recovery, share, and route features.
4. Publish curated GT1–GT10 tables.
5. Compose dashboard and AutoAI insights.
6. Review a decision pack.

The intended outputs are curated golden tables, KPI and ranked-list outputs for UK and global scope, a data dictionary, and a change log.

## Connection to implemented code and analytical contracts

The diagram describes the project intent. The current, reviewable Python/SQL implementation is linked separately: [`src/airtraffic/ingest.py`](../../../../src/airtraffic/ingest.py) loads local inputs; [`clean.py`](../../../../src/airtraffic/clean.py) normalises source-specific structures; [`golden.py`](../../../../src/airtraffic/golden.py) builds GT1–GT8; [`scoring.py`](../../../../src/airtraffic/scoring.py) builds scope- and scenario-specific candidate decisions; [`quality.py`](../../../../src/airtraffic/quality.py) evaluates reconciliation and publication checks; and [`pipeline.py`](../../../../src/airtraffic/pipeline.py) orchestrates the current run. The [GT1–GT10 contracts](../../../gt-contracts.md), [decision model](../../../decision-model.md), [lineage](../../../lineage.md), [`sql/schema.sql`](../../../../sql/schema.sql), [`sql/views.sql`](../../../../sql/views.sql), and [`sql/validation_queries.sql`](../../../../sql/validation_queries.sql) describe the actual model and SQL publication design.

Those V2 artifacts do not prove that the historical diagram's every input, handoff, or output was realised. The original archive does not contain a source export for this diagram, a historical ETL package, a Cognos report package, an AutoAI model export, or a run manifest linking the drawing to one execution. Test evidence belongs to the current code: the repository records 45 local tests, with source-dependent tests requiring private local CSVs; the public CI subset runs 11 self-contained tests. Neither count is retroactive validation of the historical process drawing.

## Decision use and limitations

The process design aims to make source preparation, measures, quality gates, and decision review explicit. It does not establish retail footfall, rent, available premises, conversion, basket size, competition, operating costs, or profitability. UK_SITE and GLOBAL_EXPANSION remain separate decision scopes; global results derived from AVI0301/ICAO data are not reproduced in this public gallery while redistribution rights remain unresolved. See the [complete 26-image evidence index](../../README.md) and [source/licensing boundary](../../../data-sources-and-licensing.md).
