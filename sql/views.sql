/*
Reporting views expose only the latest successfully PUBLISHED run.

Downstream BI tools consume reporting.* rather than physical bi.* tables.
*/

CREATE OR ALTER VIEW reporting.vw_CurrentPublishedRun
AS
SELECT TOP (1)
    run_id,
    pipeline_version,
    model_version,
    started_at_utc,
    completed_at_utc,
    published_at_utc,
    quality_failed_checks,
    quality_warning_checks
FROM meta.PipelineRun
WHERE publish_status = N'PUBLISHED'
ORDER BY
    published_at_utc DESC,
    completed_at_utc DESC,
    run_id DESC;
GO


CREATE OR ALTER VIEW reporting.vw_GT1_UK_Airport_Period_Totals
AS
SELECT t.*
FROM bi.GT1_UK_Airport_Period_Totals AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT2_UK_Airport_Period_Change
AS
SELECT t.*
FROM bi.GT2_UK_Airport_Period_Change AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT3_UK_Airport_Market_Ranking
AS
SELECT t.*
FROM bi.GT3_UK_Airport_Market_Ranking AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT4_Airport_Destination_Country_Flow
AS
SELECT t.*
FROM bi.GT4_Airport_Destination_Country_Flow AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT5_Country_Traffic_Trends
AS
SELECT t.*
FROM bi.GT5_Country_Traffic_Trends AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT6_SFO_Historical_Benchmark
AS
SELECT t.*
FROM bi.GT6_SFO_Historical_Benchmark AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT7_Global_Airport_Benchmark
AS
SELECT t.*
FROM bi.GT7_Global_Airport_Benchmark AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT8_UK_Airport_Connectivity
AS
SELECT t.*
FROM bi.GT8_UK_Airport_Connectivity AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT9_Operational_KPI_Summary
AS
SELECT t.*
FROM bi.GT9_Operational_KPI_Summary AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


CREATE OR ALTER VIEW reporting.vw_GT10_Decision_Recommendation
AS
SELECT t.*
FROM bi.GT10_Decision_Recommendation AS t
INNER JOIN reporting.vw_CurrentPublishedRun AS r
    ON r.run_id = t.run_id;
GO


/* Default executive recommendation */
CREATE OR ALTER VIEW reporting.vw_GT10_Baseline_Recommendation
AS
SELECT *
FROM reporting.vw_GT10_Decision_Recommendation
WHERE scenario = N'BASELINE';
GO


/* Top UK candidates for dashboard presentation.
   Top-N is deliberately a reporting rule, not a GT data-loss rule.
*/
CREATE OR ALTER VIEW reporting.vw_UK_Airport_Top10
AS
SELECT TOP (10) *
FROM reporting.vw_GT3_UK_Airport_Market_Ranking
ORDER BY rank;
GO


/* Top destination-country flows for dashboard presentation */
CREATE OR ALTER VIEW reporting.vw_Destination_Flow_Top10
AS
SELECT TOP (10) *
FROM reporting.vw_GT4_Airport_Destination_Country_Flow
ORDER BY passengers_current DESC;
GO
