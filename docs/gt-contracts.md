# Golden Table Contracts

## Purpose

GT1–GT10 form the governed analytical contract between the transformation
layer, Azure SQL, and downstream BI consumers.

The V2 implementation preserves lineage to the original BI solution while
correcting semantic, quality, and modelling weaknesses discovered during
refactoring.

The golden layer must not contain fabricated values, hidden assumptions, or
presentation-only filtering such as hard-coded Top 10 truncation unless the
table contract explicitly requires it.

---

## Source systems

| Source ID | Dataset | Current local coverage | Primary analytical role |
|---|---|---|---|
| AVI0105 | UK international passenger movements by country | 2013–2023 | Long-term country demand context |
| AVI0301 | International airport benchmark | 2021–2022 | Global airport comparison |
| SFO | San Francisco passenger statistics | 2005–2020 | External historical benchmark |
| ROUTES | CAA international route analysis | Current comparison snapshot, including period 202205 | UK airport international network analysis |

The V2 implementation uses the actual supplied files as the source of truth.
Historical assignment descriptions are retained as provenance but do not
override observed source schemas.

---

# GT1 — UK Airport Period Totals

**Legacy name:** UK Airport Yearly Totals

**V2 contract name:** `GT1_UK_Airport_Period_Totals`

**Business purpose:** Establish the observed international passenger scale of
each UK airport for the supplied comparison period.

**Grain:** One row per UK airport.

**Primary source:** ROUTES.

**Dimensions**
- airport_name

**Measures**
- passengers_current
- passengers_prior
- absolute_change

**Quality rules**
- airport_name must be non-null
- airport_name must be unique
- passenger values must be >= 0
- totals must reconcile exactly to ROUTES source totals

**Important semantic constraint**
The ROUTES source is a comparison snapshot. GT1 must not be described as a
multi-year annual airport history.

**Downstream consumers**
- GT2
- GT3
- GT10
- BI tactical views

---

# GT2 — UK Airport Period Change

**Legacy name:** UK Airport YoY Growth

**V2 contract name:** `GT2_UK_Airport_Period_Change`

**Business purpose:** Quantify the change in international passenger demand
between the current and source-supplied prior comparison periods.

**Grain:** One row per UK airport.

**Primary sources**
- GT1
- ROUTES

**Measures**
- passengers_current
- passengers_prior
- absolute_change
- growth_pct
- zero_baseline

**Quality rules**
- passenger totals must reconcile with GT1
- growth_pct is null when prior-period passengers are zero
- zero-baseline cases must be explicitly flagged
- extreme percentage growth must not independently drive strategic ranking

**Downstream consumers**
- BI demand/change analysis
- operational monitoring
- GT10 contextual evidence

---

# GT3 — UK Airport Market Ranking

**Legacy name:** Top10 UK Airports By Intl

**V2 contract name:** `GT3_UK_Airport_Market_Ranking`

**Business purpose:** Rank the complete UK airport candidate population by
observed current-period international passenger scale.

**Grain:** One row per UK airport.

**Primary source:** GT1.

**Measures**
- passengers_current
- market_share_pct
- rank

**Quality rules**
- complete airport population must be retained
- ranks must be unique and sequential
- market_share_pct must reconcile to the GT1 represented population
- Top N filtering belongs to the BI presentation layer, not the governed table

**Downstream consumers**
- Cognos / Power BI executive views
- tactical shortlisting
- GT10

---

# GT4 — Airport Destination Country Flow

**Legacy name:** Top10 Routes By DestCountry

**V2 contract name:** `GT4_Airport_Destination_Country_Flow`

**Business purpose:** Show international passenger concentration between UK
airports and destination countries.

**Grain:** One row per UK airport × destination country.

**Primary source:** ROUTES.

**Dimensions**
- uk_airport
- destination_country

**Measures**
- passengers_current
- destination_airport_count
- airport_flow_share_pct

**Quality rules**
- no hard-coded Top 10 truncation
- passenger totals must reconcile to ROUTES
- destination_country must be non-null
- airport_flow_share_pct denominator must be documented

**Downstream consumers**
- route-market drill-down
- geographic analysis
- tactical BI

---

# GT5 — Country Traffic Trends

**Legacy name:** UK vs SFO Comparison

**V2 contract name:** `GT5_Country_Traffic_Trends`

**Business purpose:** Provide long-term international passenger demand context
by country.

**Grain:** One row per country × year.

**Primary source:** AVI0105.

**Dimensions**
- region
- country
- year

**Measures**
- passengers
- annual_growth_pct
- pct_of_total_2023

**Optional derived context**
- index_vs_2019 where a valid 2019 observation exists

**Quality rules**
- years must remain within actual supplied file coverage
- passengers must be >= 0
- no UK-airport-level recovery metric may be inferred from country-level data

**Downstream consumers**
- strategic market context
- executive BI
- international market analysis

---

# GT6 — SFO Historical Benchmark

**Legacy name:** Post Covid Recovery

**V2 contract name:** `GT6_SFO_Historical_Benchmark`

**Business purpose:** Provide an external historical aviation benchmark and
illustrate disruption/recovery patterns at SFO.

**Grain:** One row per year.

**Primary source:** SFO.

**Measures**
- domestic_passengers
- international_passengers
- total_passengers
- international_share_pct
- annual_growth_pct

**Quality rules**
- totals must reconcile to SFO source records
- Domestic + International must reconcile to total passengers
- SFO metrics are contextual and must not be presented as direct UK-airport
  equivalents

**Downstream consumers**
- executive context
- external benchmarking
- watsonx exploratory analysis

---

# GT7 — Global Airport Benchmark

**Legacy name:** Global Expansion Candidates

**V2 contract name:** `GT7_Global_Airport_Benchmark`

**Business purpose:** Compare major international airports and support the
second-stage international expansion decision.

**Grain:** One row per airport.

**Primary source:** AVI0301.

**Dimensions**
- city
- airport_name

**Measures**
- passengers_2021
- passengers_2022
- passenger_growth_pct
- aircraft_movements_2021
- aircraft_movements_2022
- aircraft_movement_growth_pct
- passengers_per_movement_2022
- passenger_scale_score
- growth_score
- movement_scale_score
- traffic_intensity_score

**Quality rules**
- no fabricated route counts
- no fabricated international-share metric
- no UK recovery proxy
- source rank must remain traceable
- derived scores must document their normalisation method

**Downstream consumers**
- global expansion decision
- GT10 GLOBAL_EXPANSION scope
- executive BI

---

# GT8 — UK Airport Connectivity & Traffic Mix

**Legacy name:** Intl Share vs Routes

**V2 contract name:** `GT8_UK_Airport_Connectivity`

**Business purpose:** Quantify the international network breadth and traffic
composition of each UK airport.

**Grain:** One row per UK airport.

**Primary source:** ROUTES.

**Measures**
- passengers_current
- destination_country_count
- destination_airport_count
- scheduled_passengers
- charter_passengers
- scheduled_share_pct
- charter_share_pct

**Quality rules**
- destination counts use distinct observed values
- scheduled + charter passenger components must be checked against total
  passengers
- no assumed international share
- no placeholder route counts

**Downstream consumers**
- tactical network analysis
- GT10 UK_SITE scope
- Cognos / Power BI monitoring

---

# GT9 — Operational KPI & Data Quality Summary

**Legacy name:** KPI Summary

**V2 contract name:** `GT9_Operational_KPI_Summary`

**Business purpose:** Provide an auditable operational view of business KPIs,
pipeline health, source coverage, and data-quality status.

**Grain:** One row per KPI × pipeline run.

**Dimensions**
- run_id
- kpi_name
- kpi_category
- status

**Measures / attributes**
- value_numeric
- value_text
- unit
- threshold where applicable
- generated_at_utc
- source_or_table
- quality_status

Numeric and textual KPI values are stored separately so downstream BI and SQL
consumers do not need to infer data types from a mixed value column.

**KPI categories**
- BUSINESS
- DATA_QUALITY
- PIPELINE
- COVERAGE

**Quality rules**
- every pipeline run receives one run_id
- failed quality gates must not be published as PASS
- source coverage and generated-table counts must be recorded
- KPI definitions must remain stable and documented

**Downstream consumers**
- operational monitoring
- QA evidence
- run auditability
- BI health page

---

# GT10 — Decision Recommendation

**Legacy name:** LWC Recommendation

**V2 contract name:** `GT10_Decision_Recommendation`

**Business purpose:** Produce auditable strategic recommendations without
mixing incomparable candidate populations.

**Grain:** One row per candidate × decision_scope × scenario × model_version.

**Decision scopes**
- `UK_SITE`
- `GLOBAL_EXPANSION`

**Required fields**
- decision_scope
- candidate_name
- passenger_score
- connectivity_score or equivalent scope-specific component
- growth_context
- operational_score or equivalent scope-specific component
- composite_score
- rank_within_scope
- recommendation_tier
- data_quality_flag
- model_version

**Quality rules**
- UK and international candidate populations must never share one
  normalisation population
- all scored metrics must be directly observed or transparently derived
- policy weights must be explicit and versioned
- sensitivity scenarios must be calculated separately
- contextual growth metrics must not silently dominate the ranking
- no fabricated recovery, international share, route count, or geography proxy
- ranking must be reproducible from governed upstream tables

**Downstream consumers**
- executive recommendation
- strategic decision pack
- Power BI / Cognos recommendation page

---

# Contract governance

Changes to:
- grain
- metric definition
- denominator
- source
- ranking logic
- weights
- candidate population

must increment the relevant analytical/model version and be documented in
`docs/decision-model.md`.

GT contracts are data-product interfaces, not temporary dataframe layouts.
