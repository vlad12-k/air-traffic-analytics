# AirTrafficAnalytics: Evidence-Driven Airport Expansion Decision Intelligence

> **Decision-support portfolio, not a live service or investment recommendation.** This case study describes the original boutique-retail expansion problem, the analytical method and findings supported by permitted sources. The canonical local run is `20261005T163644Z_33f9f4ffa323` (`VALIDATED_LOCAL`); it was not regenerated for this case study.

## 1. Executive summary

AirTrafficAnalytics was developed as an academic analytics project for a boutique retail business considering airport-based expansion. The project owner states they personally designed and built the Power BI and IBM Cognos dashboards and performed the analysis; Microsoft and IBM were the software platforms, not the authors of the dashboard work. The owner expressly authorizes publication of all 26 original archive screenshots; source attribution/conditions and historical validation limits remain documented separately.

1. **UK_SITE:** Which UK airport market is the strongest candidate for the first boutique?
2. **GLOBAL_EXPANSION:** Which non-UK airport markets should be considered for subsequent expansion?

The system turns public aviation source extracts into governed GT1–GT10 tables, quality/reconciliation checks, a versioned and explainable candidate-scoring model, SQL publication structures and a later Power BI V2 report layer. Historical evidence documents earlier IBM Cognos and Colab/Azure SQL work. For the implementation-to-evidence sequence, see the [end-to-end project walkthrough](end-to-end-project-walkthrough.md).

The repository includes all 26 exact original archive screenshots (11 Power BI, eight Cognos and seven historical engineering/process images), one separate redacted Colab derivative, source-safe outputs, metadata-only manifests and supplemental CAA-based analytics visuals. Raw CSV inputs are not bundled. Global values appearing within screenshots are historical report evidence, not current or independently reproduced conclusions.

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

The global scope has three separate weight policies. They are documented analytical policy choices. The original screenshots may display historical global values under the owner's authorization; this report does not restate them as current results. Raw source files remain excluded.

| GLOBAL_EXPANSION scenario | Passenger scale | Passenger growth | Movement scale | Traffic intensity |
|---|---:|---:|---:|---:|
| BASELINE | 0.50 | 0.20 | 0.15 | 0.15 |
| SCALE_HEAVY | 0.65 | 0.10 | 0.15 | 0.10 |
| GROWTH_HEAVY | 0.40 | 0.35 | 0.10 | 0.15 |

The DfT notes identify ICAO as the underlying source for AVI0301. The owner has authorized publication of the original authored report screenshots, but the case study does not provide raw source files or represent screenshot values as current, independently verified outputs. AVI0301 provenance and source-specific terms remain documented in [`data-sources-and-licensing.md`](data-sources-and-licensing.md).

## 4. Data and provenance

The project owner reports that the college supplied the original dataset links and learning resources for the academic work. That provenance explains access for the project, but academic access does not by itself grant public redistribution rights.

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

![Heathrow demand and destination-connectivity view from CAA outputs](evidence/visualizations/uk-site-demand-connectivity.svg)

*Original, vendor-neutral figure prepared for this portfolio from the permitted GT1, GT4 and GT8 outputs. It directly supports the UK_SITE question: what is Heathrow's observed passenger scale, and how broad is its recorded international route footprint? The prior/current values are source-defined comparison periods, not annual airport totals. The figure includes CAA attribution and the no-resale condition; it is not a Power BI/Cognos screenshot.*

The canonical UK_SITE baseline ranks Heathrow first, and the leading UK candidate remains stable across the three documented UK policy scenarios. This UK-only conclusion is based on GT2/GT8 CAA inputs; the mixed GT10 result file remains excluded from Git. The conclusion justifies further site diligence, not an unconditional store-opening recommendation.

![UK_SITE scenario sensitivity summary: Heathrow leads in all three tested scenarios](evidence/visualizations/uk-site-scenario-stability.svg)

*This independently authored figure presents only the already documented UK-only winner result; it deliberately omits the scores and does not reproduce global AVI0301-derived rankings. Scenario stability is robustness to stated policy weights, not statistical confidence or a forecast.*

GT2 also illustrates why growth percentages need context: six airports have a zero prior baseline, and other low-baseline cases can generate unusually large ratios. The model flags zero baselines and does not allow growth alone to dominate the UK baseline score.

AVI0105 adds a separate country-level view: “Spain & Canary Islands” is the largest reported 2023 grouping at 42.624 million passengers (17.7% of the 2023 total), followed by the United States at 20.381 million (8.5%). This is national country-market context, not demand at a specific UK airport.

The SFO historical series records a **71.4%** passenger decline from **57.42 million in 2019** to **16.42 million in 2020**. Because the supplied SFO data ends in 2020, it demonstrates the scale of a disruption, not the later recovery path and not a direct forecast for UK sites.

## 9. Decision implications

For the first boutique, Heathrow is the strongest **evidence-based UK market to investigate next** in the available snapshot because it leads represented passenger scale and network breadth. Gatwick and Stansted are useful comparison markets. The exceptionally high period-change ratios at some smaller airports should not outweigh scale and connectivity without further evidence.

A responsible next business step would combine these airport-market findings with evidence not present in this project: airport retail footfall, available premises, rents, lease terms, category competition, customer conversion, basket size, operating costs and the boutique’s own unit economics. Those inputs are necessary before making a commercial viability or investment decision.

The second-stage global screen is part of the model design. Historical global values appear in owner-authorized dashboard screenshots, but no current or independently reproduced global result is asserted in the narrative.

## 10. Project evolution

The diagram below is a supplemental summary of the documented sequence. It is not an original Cognos/Power BI screenshot, report export, or proof of hands-on use of any specific platform. The separate original capture archive is inventoried in the [evidence index](evidence/README.md).

![Supplementary project chronology diagram, not platform-usage evidence](evidence/visualizations/project-evolution-timeline.svg)

*This explanatory graphic does not replace the local Cognos, Colab or Azure captures and is not vendor-produced.*

### Stage A — IBM Cognos Analytics (historical)

According to the project owner, they personally created the Cognos dashboards, semantic model and analysis as academic work; IBM Cognos was the reporting platform, not the dashboard author. The historical reports covered executive summary, demand/recovery, filtering, operations and risk-oriented views. They document an earlier implementation of the airport-retail decision problem, not a current Cognos deployment.

The public Cognos gallery contains all eight exact original archive images: the semantic model, UK demand filter/recovery, executive pages, operational monitoring/filtering and risk ranking. All ten current/prior passenger pairs in the two UK demand views match the preserved GT1 output derived from CAA Table 12.1 (comparison period 202205), but that match does not recover the historical Cognos queries, joins, refresh path or other calculations. The remaining scores and source lineage are discussed with explicit uncertainty in the [Cognos gallery notes](evidence/historical/cognos/technical-notes.md). No Cognos package, query definitions or historical source data are available for independent replay. The ZIP remains unchanged; the owner's authorization and per-image evidence are in the [historical index](evidence/historical/README.md).

![Original IBM Cognos semantic-model screenshot](evidence/historical/cognos/historical-cognos-07-semantic-model.png)

*Authentic archive capture of the project owner's Cognos semantic-model work. IBM Cognos UI is visible; no IBM permission or endorsement is claimed.*

![Original IBM Cognos UK demand-filter screenshot](evidence/historical/cognos/historical-cognos-11-demand-filter.png)

*Authentic archive capture of the project owner's UK demand filter. Source: UK CAA Table 12.1, May 2022; attribution and no-resale conditions apply. IBM Cognos UI is visible; no IBM permission or endorsement is claimed.*

![Original IBM Cognos UK airport demand-recovery screenshot](evidence/historical/cognos/historical-cognos-10-demand-recovery-original.png)

*Authentic original of the historical two-period UK demand comparison. Its ten current/prior airport passenger pairs match the preserved GT1 CAA-derived output; the original Cognos query and non-passenger calculations are not available. CAA attribution/no-resale conditions apply. No IBM endorsement is claimed.*

### Stage B — Colab, Python and Azure SQL (historical)

The archive records a notebook-based ETL/upload workflow and SQL validation activity. These are historical stages, not live services. The [historical gallery](evidence/historical/README.md) includes the exact original Colab and Azure SQL screenshots; the redacted Colab derivative is separately shown as an optional comparison, not a replacement. The current V2 code is separate and does not retroactively validate these historical screens.

### Stage C — Governed Python/SQL V2

The current analytical package introduced modular transformations, GT contracts, quality gates, reconciliation, model versioning and run provenance. The root-level legacy `main.py` prototype is excluded from the public candidate because it contains unvalidated placeholder scoring assumptions; the package under `src/airtraffic` is the canonical implementation.

### Stage D — Power BI V2

According to the project owner, they authored the Power BI V2 report design and analysis; Microsoft Power BI was the platform, not the report author. The 11 original archive screenshots cover executive, UK demand, destination/connectivity, global benchmark, scenario, governance, candidate-detail and model/relationship views. They document historical dashboard evidence, not a live deployment. No direct technical migration from Cognos to Power BI is claimed.

The featured original dashboard captures below are exact PNGs from the archive, not reconstructions. The project owner authorizes displaying their report work. CAA source attribution and no-sale conditions are preserved where applicable; no vendor endorsement is claimed.

#### UK market demand

![Original Power BI V2 UK market-demand page](evidence/power-bi-v2/powerbi-v2-02-uk-market-demand.png)

*Business question: how do represented UK airport markets compare in current and prior-period route passenger demand? Source: UK CAA Table 12.1, May 2022; CAA source reference and no-resale conditions apply. The image preserves the original report page and Power BI UI; no Microsoft permission or endorsement is claimed.*

#### UK_SITE scenario sensitivity

![Original Power BI V2 UK_SITE scenario page](evidence/power-bi-v2/powerbi-v2-05b-scenario-sensitivity-uk.png)

*Business question: does the UK_SITE leading candidate change under volume-heavy or connectivity-heavy weights? This is the original user-created scenario page; ranking is sensitivity to assumptions, not a profitability forecast. Source: UK CAA Table 12.1, May 2022; source reference and no-resale conditions apply. No Microsoft permission or endorsement is claimed.*

#### Heathrow candidate detail

![Original Power BI V2 Heathrow candidate-detail page](evidence/power-bi-v2/powerbi-v2-07b-candidate-detail-heathrow.png)

*Business question: which demand and connectivity evidence supports the Heathrow UK_SITE screen? The original authored report page displays CAA-derived measures. Source: UK CAA Table 12.1, May 2022; source reference and no-resale conditions apply. No Microsoft permission or endorsement is claimed.*

The complete [Power BI original-image gallery](evidence/power-bi-v2/technical-notes.md) includes destination connectivity, executive/global pages, governance and all remaining archive screenshots. The project contains no `.pbix`, `.pbit` or PDF export from which a UI-free report artifact could be prepared.

The two public schema captures below show the V2 semantic structure without data rows. They document model design, not airport performance.

| Semantic model | Relationships |
|---|---|
| ![Original Power BI semantic model overview](evidence/power-bi-v2/powerbi-v2-08-semantic-model-overview-archive-original.png) | ![Original Power BI relationships overview](evidence/power-bi-v2/powerbi-v2-09-relationships-overview-archive-original.png) |

The semantic-model and relationship images are the exact archive originals and are included in the same complete 11-image gallery. Their screenshots evidence model views only; they are not a machine-readable model or proof of deployed service behavior.

## 11. Validation, reproducibility and limitations

- The canonical run is recorded as `VALIDATED_LOCAL`; the repository records a 45-test local suite, including source-dependent tests. Coverage is not configured.
- A clean clone cannot run the full pipeline/tests without the four local source CSVs. They are intentionally not bundled; AVI0301 rights are unresolved.
- CAA-derived data may be included only with source reference and subject to the CAA no-sale condition. DfT and DataSF sources retain their stated terms. None of these data terms are extended or replaced by the code MIT license.
- The original academic report/business-requirements deck and formal stakeholder matrix were not found in this project folder. This case study uses the repository docs, code, manifests, canonical outputs and historical screenshots; unstated business requirements are not invented.
- The public evidence set is reduced by design. Original local screenshots, restricted tables and canonical run artifacts remain preserved locally and are not downloadable from the public repository.
- No live Azure, Cognos, watsonx or Power BI deployment, scheduled refresh, commercial store performance, or causal/forecast result is claimed.
