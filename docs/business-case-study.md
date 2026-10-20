# AirTrafficAnalytics: Evidence-Driven Airport Expansion Decision Intelligence

> **Decision-support portfolio, not a live service or investment recommendation.** This case study describes the original boutique-retail expansion problem, the analytical method and findings supported by permitted sources. The canonical local run is `20261005T163644Z_33f9f4ffa323` (`VALIDATED_LOCAL`); it was not regenerated for this case study.

## 1. Executive summary

AirTrafficAnalytics was built to help a boutique retail business decide where airport-based expansion deserved further investigation. The project treats the work as a sequence of two business decisions—not simply an aviation-statistics dashboard:

1. **UK_SITE:** Which UK airport market is the strongest candidate for the first boutique?
2. **GLOBAL_EXPANSION:** Which non-UK airport markets should be considered for subsequent expansion?

The system turns public aviation source extracts into governed GT1–GT10 tables, quality/reconciliation checks, a versioned and explainable candidate-scoring model, SQL publication structures and a later Power BI V2 report layer. Historical evidence documents earlier IBM Cognos and Colab/Azure SQL work.

The public repository is a deliberately reduced evidence package. It includes the CAA/DfT/SFO outputs whose terms are documented, manifests containing hashes and file sizes only, two schema-only Power BI screenshots, and an independently authored CAA-based market chart. Raw sources and AVI0301-dependent results remain local because the underlying ICAO redistribution rights are unresolved.

## 2. Business concept and problem

The concept is a boutique retail operation using airport markets as possible locations. The initial question is whether a UK airport offers a large, connected passenger market for a first site; the second is whether later international markets merit further analysis.

A useful decision process needs more than passenger totals. It should distinguish market scale from network breadth, describe where international passengers travel, show the limits of period comparisons, and make candidate-scoring assumptions visible. It should also avoid presenting airport traffic as proof of store sales, lease availability or profitability.

### Stakeholders and requirements evidence

The project files do not contain a separate formal stakeholder matrix, signed business-requirements document or original academic report deck. Based on the documented decision scopes, the implied business decision owner is the boutique owner or expansion leadership; BI/analytics users maintain the data model, quality controls and reporting. This is an inference from the project materials, not a recovered RACI.

The requirements supported by the available files are:

- shortlist UK airport markets for the first boutique;
- evaluate a separate non-UK population for later expansion;
- use observed passenger demand and connectivity evidence;
- keep market definitions, denominators and candidate populations explicit;
- explain rankings through governed features and policy weights;
- test sensitivity to alternative business priorities;
- preserve lineage, quality checks, run provenance and decision limitations.

## 3. Decision scopes

### UK_SITE — first boutique location

The UK candidate population consists of airports in the supplied CAA route-analysis layer. GT1–GT4 and GT8 represent period demand, relative market position, airport-to-destination-country flows, network breadth and scheduled/charter mix. GT2 records the supplied current/prior comparison and flags zero-baseline cases.

The baseline policy weights are 50% passenger scale, 30% destination-country breadth and 20% destination-airport breadth. Two alternatives show how executive priorities change the decision:

| UK_SITE scenario | Passenger scale | Country breadth | Airport breadth |
|---|---:|---:|---:|
| BASELINE | 0.50 | 0.30 | 0.20 |
| VOLUME_HEAVY | 0.65 | 0.20 | 0.15 |
| CONNECTIVITY_HEAVY | 0.35 | 0.35 | 0.30 |

Growth is contextual rather than a dominant baseline component because small or zero prior-period denominators can produce extreme ratios.

### GLOBAL_EXPANSION — later international markets

The model design compares AVI0301/GT7 candidates on passenger scale, passenger growth, aircraft movement scale and passengers per movement. It excludes airports already represented in UK_SITE through a deterministic cross-source eligibility check, then normalizes within the global candidate population. Passenger-per-movement is an intensity measure, not a profitability proxy.

The global scope has three separate weight policies. They are documented analytical policy choices, but no global result values are published while the source rights are unresolved.

| GLOBAL_EXPANSION scenario | Passenger scale | Passenger growth | Movement scale | Traffic intensity |
|---|---:|---:|---:|---:|
| BASELINE | 0.50 | 0.20 | 0.15 | 0.15 |
| SCALE_HEAVY | 0.65 | 0.10 | 0.15 | 0.10 |
| GROWTH_HEAVY | 0.40 | 0.35 | 0.10 | 0.15 |

The DfT notes identify ICAO as the underlying source for AVI0301, but the project does not contain verified redistribution permission for that exact extract or its derivatives. Accordingly, this case study gives no global airport names, rankings, benchmark values or recommendation. The method is described; the source-dependent outcomes remain local-only. See [`data-sources-and-licensing.md`](data-sources-and-licensing.md).

## 4. Data and provenance

| Source | Analytical role | Local coverage | Important limitation |
|---|---|---|---|
| DfT AVI0105 | Country-level UK international passenger trends | 2013–2023 | National/country context, not individual-airport recovery. Attribution and table notes apply. |
| DfT AVI0301 (ICAO-sourced) | Global airport benchmark | 2021–2022 | Rights unresolved for the exact ICAO-originated extract and derivatives; public values are withheld. |
| CAA Table 12.1 (`ROUTES`) | UK airport × international destination flows and comparison-period passenger counts | CAA comparison period `202205` with its supplied prior period | A route-analysis snapshot, not a multi-year annual airport history. CAA requires reference and prohibits resale of its statistics. |
| SFO Air Traffic Passenger Statistics (DataSF) | External historical domestic/international benchmark | 2005–2020 | Historical and geographically distinct; it is context, not a direct UK-airport proxy. |

The project manifest records the local input file names, sizes and SHA-256 hashes. The public copy contains no source rows. The `AVI0301` sample schema and all row-level source details remain local. The raw datasets are not bundled; source terms and attribution rules are summarized in the [licensing inventory](data-sources-and-licensing.md).

## 5. Analytical questions and GT1–GT10 contracts

The GT tables form a governed interface between Python transformations, SQL and BI consumers:

| Table | Responsibility | Business use |
|---|---|---|
| GT1 | UK airport current/prior passenger totals | Compare market scale in the supplied CAA snapshot |
| GT2 | Absolute and percentage period change; zero-baseline flag | Interpret changes without treating tiny baselines as stable growth |
| GT3 | Complete represented UK-airport population, market share and rank | Screen relative passenger scale; Top-N belongs in presentation, not source truncation |
| GT4 | Airport × destination-country passenger flow | Describe destination mix and concentration |
| GT5 | Country × year passenger trend | Provide long-term demand context from AVI0105 |
| GT6 | Annual SFO domestic/international totals and growth | Provide historical disruption context |
| GT7 | Global airport passenger/movement benchmark | Inputs to GLOBAL_EXPANSION; data values withheld pending rights clearance |
| GT8 | UK airport connectivity and scheduled/charter mix | Describe destination breadth and traffic composition |
| GT9 | Per-run operational, coverage and data-quality KPIs | Monitor pipeline and QA state |
| GT10 | Candidate × decision scope × scenario × model version | Store explainable UK/global recommendations and sensitivity results |

The model does not infer airport-level recovery from country-level AVI0105, assume international share, fabricate route counts, treat a percentile score as a probability, or turn traffic intensity into profitability.

## 6. ETL, governance and BI architecture

```text
AVI0105 / AVI0301 / CAA ROUTES / SFO
                  ↓
Python ingestion, source profiling, cleaning and standardisation
                  ↓
Feature engineering, governed GT1–GT8 and reconciliation
                  ↓
GT10 scope-specific scoring and scenario sensitivity
                  ↓
Quality gates, GT9, run metadata and local validated exports
                  ↓
Run-aware SQL schemas/views (publication design)
                  ↓
Power BI V2 reporting layer
```

The V2 Python package separates ingestion, cleaning, eligibility, metrics, scoring, quality checks, provenance and export. SQL defines `meta`, `bi` and `reporting` structures, including latest-published-run views and validation queries. Azure publication is a separate credentialed operation; it was not performed for this case study.

The canonical run metadata records `VALIDATED_LOCAL`, 30 quality checks, zero failures and zero warnings. The source/artifact manifests were verified against local file sizes and hashes. This is archived local evidence, not a freshly rerun result or evidence that Azure, Cognos or Power BI is currently live.

## 7. Candidate scoring and sensitivity

UK_SITE ranks candidates using within-scope percentile scores for passenger scale, destination-country breadth and destination-airport breadth. The baseline and two alternative policies expose the trade-off between volume and connectivity. Each score is relative to the represented UK population and depends on policy weights.

GLOBAL_EXPANSION uses a separate candidate set and separate percentile normalization. Its component features are passenger scale, passenger growth, aircraft movement scale and passengers per movement. Since its input lineage includes AVI0301/ICAO, its scores and ranks are deliberately omitted from this public case study; they are not reconstructed or replaced.

Sensitivity analysis checks whether a top candidate changes under the documented policy weights. It tests robustness to business assumptions—not statistical confidence, causality or forecast accuracy.

## 8. Evidence-backed UK findings

The chart below is an original, independently authored visualization from the canonical, permitted GT3 output—not a Power BI/Cognos screenshot. It displays only the CAA UK_SITE market snapshot, with the CAA source and no-resale condition shown in the figure.

![UK airport market snapshot from CAA GT3 output](evidence/visualizations/uk-airport-market-snapshot.svg)

In the represented 36-airport CAA population, the current comparison-period total is **17,984,754** passengers versus **1,178,740** in the supplied prior period. Heathrow is the largest market in GT3 at **4,993,568** passengers and **27.77%** of the represented total, followed by Gatwick, Stansted, Manchester and Luton. The share is not the share of all UK aviation or retail spending.

GT8 shows Heathrow with **90** destination countries and **207** distinct destination airports in this source snapshot. In GT4, the largest Heathrow destination-country flow is the United States. These measures describe scale and reach; they do not show the proportion of travelers who would visit a boutique.

The canonical UK_SITE baseline ranks Heathrow first, and the leading UK candidate remains stable across the three documented UK policy scenarios. This UK-only conclusion is based on GT2/GT8 CAA inputs; the mixed GT10 result file remains excluded from Git. The conclusion justifies further site diligence, not an unconditional store-opening recommendation.

GT2 also illustrates why growth percentages need context: six airports have a zero prior baseline, and other low-baseline cases can generate unusually large ratios. The model flags zero baselines and does not allow growth alone to dominate the UK baseline score.

AVI0105 adds a separate country-level view: “Spain & Canary Islands” is the largest reported 2023 grouping at 42.624 million passengers (17.7% of the 2023 total), followed by the United States at 20.381 million (8.5%). This is national country-market context, not demand at a specific UK airport.

The SFO historical series records a **71.4%** passenger decline from **57.42 million in 2019** to **16.42 million in 2020**. Because the supplied SFO data ends in 2020, it demonstrates the scale of a disruption, not the later recovery path and not a direct forecast for UK sites.

## 9. Decision implications

For the first boutique, Heathrow is the strongest **evidence-based UK market to investigate next** in the available snapshot because it leads represented passenger scale and network breadth. Gatwick and Stansted are useful comparison markets. The exceptionally high period-change ratios at some smaller airports should not outweigh scale and connectivity without further evidence.

A responsible next business step would combine these airport-market findings with evidence not present in this project: airport retail footfall, available premises, rents, lease terms, category competition, customer conversion, basket size, operating costs and the boutique’s own unit economics. Those inputs are necessary before making a commercial viability or investment decision.

The second-stage global screen is part of the model design, but no public global candidate result is asserted while AVI0301 redistribution rights remain unresolved.

## 10. Project evolution

### Stage A — IBM Cognos Analytics (historical)

The local evidence archive documents an initial semantic model and executive, demand, filter, operational and risk-oriented Cognos views. Cognos screenshots remain local-only because the project has no documented IBM screenshot-reuse permission; some also contain source-derived data. They are not evidence of a currently running Cognos environment.

### Stage B — Colab, Python and Azure SQL (historical)

The archived evidence records a notebook-based ETL/upload workflow and SQL validation activity. The Colab/Azure screenshots and result grids remain local because of data lineage, privacy and unverified vendor screenshot rights. No Azure service is claimed to be active.

### Stage C — Governed Python/SQL V2

The current analytical package introduced modular transformations, GT contracts, quality gates, reconciliation, model versioning and run provenance. The root-level legacy `main.py` prototype is excluded from the public candidate because it contains unvalidated placeholder scoring assumptions; the package under `src/airtraffic` is the canonical implementation.

### Stage D — Power BI V2

The later report layer contains executive, UK demand, destination/connectivity, global benchmark, scenario, governance and candidate-detail pages, plus semantic-model and relationships views. Only the unchanged, schema-only model/relationship screenshots are included. Data-bearing report captures are withheld because screenshot terms and/or third-party content restrictions are not cleared. This documents sequential implementations of a similar business workflow; no direct technical migration from Cognos to Power BI is claimed.

## 11. Validation, reproducibility and limitations

- The canonical run is recorded as `VALIDATED_LOCAL`; the test suite passed 37 tests in the local environment with source inputs available. Coverage is not configured.
- A clean clone cannot run the full pipeline/tests without the four local source CSVs. They are intentionally not bundled; AVI0301 rights are unresolved.
- CAA-derived data may be included only with source reference and subject to the CAA no-sale condition. DfT and DataSF sources retain their stated terms. None of these data terms are extended or replaced by the code MIT license.
- The original academic report/business-requirements deck and formal stakeholder matrix were not found in this project folder. This case study uses the repository docs, code, manifests, canonical outputs and historical screenshots; unstated business requirements are not invented.
- The public evidence set is reduced by design. Original local screenshots, restricted tables and canonical run artifacts remain preserved locally and are not downloadable from the public repository.
- No live Azure, Cognos, watsonx or Power BI deployment, scheduled refresh, commercial store performance, or causal/forecast result is claimed.
