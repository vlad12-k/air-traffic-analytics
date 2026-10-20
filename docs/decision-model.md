# Decision Model

## Objective

GT10 provides decision support for two different business decisions:

1. selecting a UK airport for the first boutique;
2. prioritising an international airport for later expansion.

These are separate analytical populations and must be scored independently.

## GT10 storage grain

GT10 uses long-form scenario storage:

`candidate × decision_scope × scenario × model_version`

This preserves every sensitivity scenario as an auditable analytical record.
The BASELINE scenario represents the default executive recommendation, while
alternative scenarios test ranking robustness under different business policy
weights.

The model is intentionally explainable. Complex modelling is only justified
where it improves decision quality and remains auditable.

---

# Scope A — UK_SITE

## Candidate population

All UK airports represented in the governed ROUTES analytical layer.

## Core scored dimensions

### Passenger scale
Observed current-period international passenger volume.

Source:
- GT1
- GT8

Purpose:
Represents accessible passenger market scale.

### Destination-country breadth
Number of distinct observed destination countries.

Source:
- GT8

Purpose:
Represents international market diversity.

### Destination-airport breadth
Number of distinct observed destination airports.

Source:
- GT8

Purpose:
Represents network connectivity.

## Contextual dimensions

### Period change
Current versus supplied prior comparison-period growth.

Source:
- GT2

This is reported but is not permitted to dominate the baseline score because
small or zero prior-period denominators can create extreme percentages.

### Scheduled / charter mix
Reported as decision context.

Source:
- GT8

It is not included in the baseline composite score unless a documented
business requirement establishes a defensible preference.

---

# Scope B — GLOBAL_EXPANSION

## Candidate population

Airports represented in AVI0301 / GT7, excluding airports identified as part
of the observed UK_SITE airport population.

Eligibility is determined through a deterministic cross-source airport-name
crosswalk against GT8. The original source labels remain unchanged; the
canonical comparison key is used only for eligibility matching.

Excluded candidates remain auditable through the GT10 eligibility report.

This prevents the second-stage GLOBAL_EXPANSION decision from recommending
the same UK market already covered by the UK_SITE decision scope.

## Core scored dimensions

### Passenger scale
2022 passenger volume.

### Passenger growth
2021–2022 passenger percentage growth.

### Aircraft movement scale
2022 aircraft movements.

### Traffic intensity
Passengers per aircraft movement.

Traffic intensity is derived as:

passengers_2022 / aircraft_movements_2022

It is an operational intensity indicator, not a profitability measure.

---

# Normalisation

Component scoring uses within-scope percentile ranking by default.

Reasons:
- metrics use different units;
- large absolute aviation hubs can otherwise dominate all dimensions;
- percentile ranking is interpretable;
- it reduces sensitivity to extreme raw magnitudes.

Raw metrics remain available beside normalised scores.

No normalised score may be compared across decision scopes.

---

# Policy scenarios

Weights are policy parameters rather than hidden constants.

## UK_SITE

### BASELINE
- passenger_scale: 0.50
- country_breadth: 0.30
- route_breadth: 0.20

### VOLUME_HEAVY
- passenger_scale: 0.65
- country_breadth: 0.20
- route_breadth: 0.15

### CONNECTIVITY_HEAVY
- passenger_scale: 0.35
- country_breadth: 0.35
- route_breadth: 0.30

## GLOBAL_EXPANSION

### BASELINE
- passenger_scale: 0.50
- passenger_growth: 0.20
- movement_scale: 0.15
- traffic_intensity: 0.15

### SCALE_HEAVY
- passenger_scale: 0.65
- passenger_growth: 0.10
- movement_scale: 0.15
- traffic_intensity: 0.10

### GROWTH_HEAVY
- passenger_scale: 0.40
- passenger_growth: 0.35
- movement_scale: 0.10
- traffic_intensity: 0.15

Scenario weights must sum to 1.00.

---

# Sensitivity analysis

Each decision scope is evaluated under all defined policy scenarios.

The pipeline records:
- candidate rank per scenario
- composite score per scenario
- top-candidate stability
- rank range across scenarios

A recommendation is more robust when the same candidate remains near the top
under materially different policy assumptions.

Sensitivity analysis does not manufacture statistical confidence. It tests
decision robustness to documented policy weights.

---

# Recommendation tiers

Recommendation tiers are presentation labels, not probability estimates.

- `PRIMARY` — rank 1 within scope
- `SHORTLIST` — ranks 2–3
- `REVIEW` — remaining eligible candidates

---

# Data-quality flags

Possible values include:

- `PASS`
- `ZERO_BASELINE_CONTEXT`
- `MISSING_COMPONENT`
- `SOURCE_LIMITATION`

A candidate with an unresolved missing scored component must not silently
receive a neutral score.

---

# Model governance

Current model family:

`BI_DECISION_V2`

Every material change to:
- candidate population
- feature definition
- normalisation
- weight policy
- exclusion rule

requires a model-version change.

The model must remain reproducible from GT1–GT8 and the published policy
configuration.
