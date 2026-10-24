# Power BI V2 — technical walkthrough of published original screenshots

These are the five original PNGs already present in the public evidence gallery: three owner-authored report pages and two unchanged, schema-only pages. The owner authorizes publication of their report work; that does not claim Microsoft permission or endorsement. The CAA-derived captures retain the source attribution/no-resale conditions. No live Power BI service, refresh, PBIX, or deployment is claimed.

The sequence follows the decision workflow: inspect the UK market → test policy sensitivity → inspect the leading candidate → review model structure.

## 1. UK market demand — scope and period comparison

![Original Power BI V2 UK market demand page](powerbi-v2-02-uk-market-demand.png)

**Business question.** Which represented UK airport has the strongest observed passenger market for the first UK_SITE boutique screen, and how does the selected market compare with its supplied prior period?

**Design and visible evidence.** The page presents a UK airport selector, current/prior passenger KPIs, airport ranking, market-share and traffic-share views, and a selected-airport comparison. The captured selection is Heathrow. Visible values include 4,993,568 current passengers, 567,162 prior-period passengers, 4,426,406 absolute difference, 27.77% represented-market share, rank 1, and 780.45% comparison-period change. These are the displayed source-period measures, not a forecast.

**Model and transformations.** The documented V2 concepts are GT1 (`passengers_current`, `passengers_prior`, `absolute_change`), GT2 (`growth_pct` and zero-baseline context), and GT3 (`market_share_pct`, `rank`). GT1 is one row per UK airport and reconciles to ROUTES; GT2 flags zero baselines and prevents extreme percentage changes from independently driving the strategic ranking; GT3 retains the complete represented airport population. The capture is historical report evidence: this description does not assert every displayed field was directly exported from the later V2 tables.

**Interpretation and decision.** Heathrow appears as the largest market in the represented CAA comparison population. The page supports prioritising it for further site diligence, not choosing a lease or predicting retail sales.

**Validation and limitations.** Current V2 documentation specifies source-specific cleaning, GT1–GT3 reconciliation, and publication quality gates. The recorded canonical local run reports 30 checks, zero failures, and zero warnings; it was not regenerated for this image. CAA Table 12.1, May 2022, requires attribution and prohibits resale. The source is a comparison snapshot, not a multi-year airport history. The 780.45% result is sensitive to the prior-period denominator. Retail footfall, available premises, rent, conversion, basket size, competition, and operating margin are absent. Power BI UI is visible; no Microsoft permission or endorsement is claimed.

## 2. UK_SITE scenario sensitivity — policy robustness

![Original Power BI V2 UK_SITE scenario sensitivity page](powerbi-v2-05b-scenario-sensitivity-uk.png)

**Business question.** Does the preferred UK airport change when decision-makers express different priorities for passenger scale versus destination connectivity?

**Design and visible evidence.** The page displays a decision-scope control, baseline winner, scenario winner/score views, candidate sensitivity table, and ranking-stability visual. It reports three scenarios, 36 candidates, and one distinct scenario winner. Heathrow is shown as baseline winner and scores 1.00 in the visible baseline, connectivity-heavy, and volume-heavy columns. The candidate table makes comparisons inspectable rather than hiding them in a single KPI.

**Model and relationships.** The documented UK_SITE decision model uses the full represented ROUTES airport population and within-scope percentile components for passenger scale, destination-country breadth, and destination-airport breadth. Policy weights are explicit: BASELINE 0.50/0.30/0.20, VOLUME_HEAVY 0.65/0.20/0.15, and CONNECTIVITY_HEAVY 0.35/0.35/0.30. GT10 has grain candidate × decision scope × scenario × model version. Period growth is contextual and must not dominate the baseline. These contracts explain the documented decision framework; the screenshot alone does not prove a specific model refresh or implementation.

**Interpretation and decision.** The visible UK scenarios keep Heathrow at the top, suggesting robustness to these three tested policy-weight profiles. This is sensitivity to assumptions, not probability, statistical confidence, or commercial viability.

**Validation and limitations.** The project documents versioned weights, within-scope normalization, per-scenario ranking, and quality flags. The screenshot shows 36 candidates; no independent scoring rerun is evidenced here. CAA attribution/no-resale conditions apply. Only the documented policy profiles were tested; changed source coverage or different priorities may alter results. Retail economics are absent. Power BI UI is visible; no Microsoft permission or endorsement is claimed.

## 3. Heathrow candidate detail — evidence behind the screen

![Original Power BI V2 Heathrow candidate detail page](powerbi-v2-07b-candidate-detail-heathrow.png)

**Business question.** What observed market and network evidence supports Heathrow's UK_SITE rank, and does its recommendation tier remain stable across tested policies?

**Design and visible evidence.** The capture identifies Heathrow, scope `UK_SITE`, displayed data-quality flag `PASS`, baseline rank 1, and tier `PRIMARY`. It shows candidate sensitivity across BASELINE, CONNECTIVITY_HEAVY, and VOLUME_HEAVY, a component-profile view, and underlying candidate evidence. Visible measures include 4,993,568 passengers, 780.45% growth context, 90 destination countries, and 207 destination airports. The displayed model label is `BI_DECISION_V2.0.0`.

**Model and metric lineage.** Documented contracts map passenger totals/change to GT1–GT2, airport rank to GT3, and distinct destination-country/airport counts to GT8. GT10 stores a scope-specific recommendation with component scores, rank, tier, quality flag, scenario, and model version. UK_SITE baseline weights emphasize passenger scale (0.50), country breadth (0.30), and route breadth (0.20); sensitivity profiles reweight those priorities. `PRIMARY` means rank 1 within scope, not a probability of success.

**Interpretation and decision.** The page supports carrying Heathrow forward to commercial and operational diligence. The extreme percentage change is contextual and should not be read as expected growth.

**Validation and limitations.** The screenshot's `PASS` is a displayed candidate status, not evidence of a new validation run. The separately documented canonical local run reports 30 checks with no failures or warnings. CAA Table 12.1 attribution/no-resale conditions apply. The capture does not establish retail footfall, premises availability, costs, competition, or profitability. Power BI UI is visible; no Microsoft permission or endorsement is claimed.

## 4. Semantic model overview — analytical objects

![Original Power BI V2 semantic model overview](powerbi-v2-08-semantic-model-overview.png)

This unchanged, schema-only screenshot documents the semantic-model layer. The project describes GT1–GT10 as a governed interface between transformation, SQL, and BI consumers: UK market totals/change/ranking, destination flows/connectivity, operational quality, and scenario-versioned recommendations.

The screenshot contains model/schema metadata rather than source rows. It evidences a captured model view, not refresh, source lineage, measure correctness, row-level security, or a deployed service. Grain and metric definitions are in [GT1–GT10 contracts](../../gt-contracts.md) and the [decision model](../../decision-model.md). The existing evidence record identifies it as pixel-checked against the archive and includes the standard “Used with permission from Microsoft” attribution; that is not endorsement or a bespoke permission letter.

## 5. Relationships overview — model navigation

![Original Power BI V2 relationships overview](powerbi-v2-09-relationships-overview.png)

This unchanged, schema-only screenshot records the model relationship view. Relationships govern how report filters reach model objects; the image is design evidence, not a machine-readable model definition or relationship test.

No source rows are shown. The screenshot alone does not establish every key, cardinality, filter direction, ambiguity, or runtime behavior. The actual model artifact is not included here, so those details are not independently reviewable from this gallery. The existing evidence record identifies it as pixel-checked against the archive and uses the standard Microsoft screenshot attribution; no vendor endorsement or bespoke permission is claimed.

## Other original Power BI archive pages not published

The six remaining original report PNGs stay local for these individual reasons, recorded in the [complete 26-image inventory](../README.md):

- `01-executive-decision-summary.png` — global recommendation values depend on AVI0301/ICAO data with unresolved redistribution rights.
- `03-destination-connectivity.png` — CAA values plus an unattributed map layer; map-source terms remain unresolved.
- `04-global-expansion-benchmark.png` — AVI0301/ICAO benchmark results are not cleared for redistribution.
- `05a-scenario-global-expansion.png` — global scenario results depend on the same uncleared source.
- `06-data-quality-governance.png` — includes AVI0301/global-source counts.
- `07a-candidate-detail-dubai.png` — global candidate results depend on the same uncleared source.

The owner's authorship authorization does not clear third-party source-data or map-provider rights. No screenshot was recreated, redacted, or replaced with a diagram.