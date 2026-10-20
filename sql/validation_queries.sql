/*
Independent post-publication validation.

Expected result:
- all reconciliation deltas = 0
- market share ≈ 100
- no duplicate GT10 grain
- no invalid policy weights
- one BASELINE PRIMARY candidate per decision scope
*/

SET NOCOUNT ON;

DECLARE @run_id NVARCHAR(64);

SELECT TOP (1)
    @run_id = run_id
FROM meta.PipelineRun
WHERE publish_status = N'PUBLISHED'
ORDER BY
    published_at_utc DESC,
    completed_at_utc DESC,
    run_id DESC;

SELECT
    N'Validated run' AS check_name,
    @run_id AS run_id;


/* ============================================================
   TABLE COUNTS
   ============================================================ */

SELECT
    N'GT1' AS table_name,
    COUNT(*) AS row_count
FROM bi.GT1_UK_Airport_Period_Totals
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT2',
    COUNT(*)
FROM bi.GT2_UK_Airport_Period_Change
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT3',
    COUNT(*)
FROM bi.GT3_UK_Airport_Market_Ranking
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT4',
    COUNT(*)
FROM bi.GT4_Airport_Destination_Country_Flow
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT5',
    COUNT(*)
FROM bi.GT5_Country_Traffic_Trends
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT6',
    COUNT(*)
FROM bi.GT6_SFO_Historical_Benchmark
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT7',
    COUNT(*)
FROM bi.GT7_Global_Airport_Benchmark
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT8',
    COUNT(*)
FROM bi.GT8_UK_Airport_Connectivity
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT9',
    COUNT(*)
FROM bi.GT9_Operational_KPI_Summary
WHERE run_id = @run_id

UNION ALL

SELECT
    N'GT10',
    COUNT(*)
FROM bi.GT10_Decision_Recommendation
WHERE run_id = @run_id;


/* ============================================================
   PASSENGER RECONCILIATION
   ============================================================ */

WITH totals AS (
    SELECT
        (
            SELECT SUM(passengers_current)
            FROM bi.GT1_UK_Airport_Period_Totals
            WHERE run_id = @run_id
        ) AS gt1_total,

        (
            SELECT SUM(passengers_current)
            FROM bi.GT4_Airport_Destination_Country_Flow
            WHERE run_id = @run_id
        ) AS gt4_total,

        (
            SELECT SUM(passengers_current)
            FROM bi.GT8_UK_Airport_Connectivity
            WHERE run_id = @run_id
        ) AS gt8_total
)
SELECT
    gt1_total,
    gt4_total,
    gt8_total,
    gt4_total - gt1_total AS gt4_delta,
    gt8_total - gt1_total AS gt8_delta
FROM totals;


/* ============================================================
   GT3 MARKET SHARE
   ============================================================ */

SELECT
    SUM(market_share_pct) AS market_share_total,
    ABS(
        SUM(market_share_pct) - 100.0
    ) AS market_share_delta
FROM bi.GT3_UK_Airport_Market_Ranking
WHERE run_id = @run_id;


/* ============================================================
   GT6 CLASSIFICATION
   ============================================================ */

SELECT
    SUM(ABS(classification_delta))
        AS absolute_classification_delta
FROM bi.GT6_SFO_Historical_Benchmark
WHERE run_id = @run_id;


/* ============================================================
   GT8 COMPONENT RECONCILIATION
   ============================================================ */

SELECT
    SUM(ABS(component_reconciliation_delta))
        AS absolute_component_delta
FROM bi.GT8_UK_Airport_Connectivity
WHERE run_id = @run_id;


/* ============================================================
   GT10 GRAIN
   Expected duplicate rows = 0
   ============================================================ */

SELECT
    decision_scope,
    scenario,
    candidate_name,
    model_version,
    COUNT(*) AS duplicate_count
FROM bi.GT10_Decision_Recommendation
WHERE run_id = @run_id
GROUP BY
    decision_scope,
    scenario,
    candidate_name,
    model_version
HAVING COUNT(*) > 1;


/* ============================================================
   GT10 POLICY WEIGHTS
   Expected invalid rows = 0
   ============================================================ */

SELECT
    COUNT(*) AS invalid_weight_rows
FROM bi.GT10_Decision_Recommendation
WHERE run_id = @run_id
  AND ABS(
        weight_passenger_scale
        + weight_country_breadth
        + weight_route_breadth
        + weight_passenger_growth
        + weight_movement_scale
        + weight_traffic_intensity
        - 1.0
      ) > 0.000000001;


/* ============================================================
   GT10 SCORE BOUNDS
   Expected invalid rows = 0
   ============================================================ */

SELECT
    COUNT(*) AS invalid_score_rows
FROM bi.GT10_Decision_Recommendation
WHERE run_id = @run_id
  AND data_quality_flag = N'PASS'
  AND (
        composite_score IS NULL
        OR composite_score < 0
        OR composite_score > 1
      );


/* ============================================================
   ONE BASELINE PRIMARY PER DECISION SCOPE
   Expected:
     GLOBAL_EXPANSION = 1
     UK_SITE          = 1
   ============================================================ */

SELECT
    decision_scope,
    COUNT(*) AS primary_count
FROM bi.GT10_Decision_Recommendation
WHERE run_id = @run_id
  AND scenario = N'BASELINE'
  AND recommendation_tier = N'PRIMARY'
GROUP BY decision_scope;


/* ============================================================
   BASELINE RECOMMENDATIONS
   ============================================================ */

SELECT
    decision_scope,
    candidate_name,
    composite_score,
    rank_within_scope,
    data_quality_flag,
    model_version
FROM bi.GT10_Decision_Recommendation
WHERE run_id = @run_id
  AND scenario = N'BASELINE'
ORDER BY
    decision_scope,
    rank_within_scope;


/* ============================================================
   PIPELINE QUALITY AUDIT
   ============================================================ */

SELECT
    status,
    severity,
    COUNT(*) AS check_count
FROM meta.QualityCheck
WHERE run_id = @run_id
GROUP BY
    status,
    severity
ORDER BY
    severity,
    status;


/* ============================================================
   GT9 PUBLISH STATUS
   ============================================================ */

SELECT
    kpi_name,
    value_numeric,
    value_text,
    unit,
    status
FROM bi.GT9_Operational_KPI_Summary
WHERE run_id = @run_id
  AND kpi_category IN (
        N'DATA_QUALITY',
        N'PIPELINE'
      )
ORDER BY
    kpi_category,
    kpi_name;
