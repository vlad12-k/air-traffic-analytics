/*
Air Traffic Analytics V2
Governed Azure SQL analytical layer.

Schemas:
  meta      - pipeline execution and data-quality audit
  bi        - governed GT1-GT10 analytical tables
  reporting - downstream semantic/reporting views (created separately)

Publishing model:
  - every analytical row belongs to a run_id
  - only a successfully validated run may become PUBLISHED
  - reporting views expose the latest PUBLISHED run
*/

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = N'meta'
)
    EXEC(N'CREATE SCHEMA meta');
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = N'bi'
)
    EXEC(N'CREATE SCHEMA bi');
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.schemas
    WHERE name = N'reporting'
)
    EXEC(N'CREATE SCHEMA reporting');
GO


/* ============================================================
   PIPELINE AUDIT
   ============================================================ */

IF OBJECT_ID(N'meta.PipelineRun', N'U') IS NULL
BEGIN
    CREATE TABLE meta.PipelineRun (
        run_id                  NVARCHAR(64)  NOT NULL,
        pipeline_version        NVARCHAR(32)  NOT NULL,
        model_version           NVARCHAR(64)  NULL,
        started_at_utc          DATETIME2(3)  NOT NULL,
        completed_at_utc        DATETIME2(3)  NULL,
        published_at_utc        DATETIME2(3)  NULL,
        publish_status          NVARCHAR(20)  NOT NULL,
        quality_failed_checks   INT           NOT NULL DEFAULT (0),
        quality_warning_checks  INT           NOT NULL DEFAULT (0),
        source_manifest_sha256  CHAR(64)      NULL,

        CONSTRAINT PK_PipelineRun
            PRIMARY KEY (run_id),

        CONSTRAINT CK_PipelineRun_Status
            CHECK (
                publish_status IN (
                    N'RUNNING',
                    N'VALIDATED',
                    N'PUBLISHED',
                    N'FAILED'
                )
            ),

        CONSTRAINT CK_PipelineRun_QualityCounts
            CHECK (
                quality_failed_checks >= 0
                AND quality_warning_checks >= 0
            )
    );
END;
GO


IF OBJECT_ID(N'meta.QualityCheck', N'U') IS NULL
BEGIN
    CREATE TABLE meta.QualityCheck (
        run_id          NVARCHAR(64)   NOT NULL,
        check_id        NVARCHAR(100)  NOT NULL,
        category        NVARCHAR(50)   NOT NULL,
        object_name     NVARCHAR(128)  NOT NULL,
        status          NVARCHAR(10)   NOT NULL,
        severity        NVARCHAR(10)   NOT NULL,
        observed_value  NVARCHAR(4000) NULL,
        expected_value  NVARCHAR(4000) NULL,
        message         NVARCHAR(2000) NOT NULL,

        CONSTRAINT PK_QualityCheck
            PRIMARY KEY (run_id, check_id),

        CONSTRAINT FK_QualityCheck_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_QualityCheck_Status
            CHECK (
                status IN (
                    N'PASS',
                    N'WARN',
                    N'FAIL'
                )
            ),

        CONSTRAINT CK_QualityCheck_Severity
            CHECK (
                severity IN (
                    N'INFO',
                    N'WARNING',
                    N'ERROR'
                )
            )
    );
END;
GO


/* ============================================================
   GT1
   ============================================================ */

IF OBJECT_ID(N'bi.GT1_UK_Airport_Period_Totals', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT1_UK_Airport_Period_Totals (
        run_id              NVARCHAR(64)  NOT NULL,
        airport_name        NVARCHAR(200) NOT NULL,
        passengers_current  BIGINT        NOT NULL,
        passengers_prior    BIGINT        NOT NULL,
        absolute_change     BIGINT        NOT NULL,
        comparison_period   INT           NOT NULL,

        CONSTRAINT PK_GT1
            PRIMARY KEY (run_id, airport_name),

        CONSTRAINT FK_GT1_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT1_Passengers
            CHECK (
                passengers_current >= 0
                AND passengers_prior >= 0
            )
    );
END;
GO


/* ============================================================
   GT2
   ============================================================ */

IF OBJECT_ID(N'bi.GT2_UK_Airport_Period_Change', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT2_UK_Airport_Period_Change (
        run_id              NVARCHAR(64)  NOT NULL,
        airport_name        NVARCHAR(200) NOT NULL,
        passengers_current  BIGINT        NOT NULL,
        passengers_prior    BIGINT        NOT NULL,
        absolute_change     BIGINT        NOT NULL,
        comparison_period   INT           NOT NULL,
        growth_pct          DECIMAL(19,6) NULL,
        zero_baseline       BIT           NOT NULL,

        CONSTRAINT PK_GT2
            PRIMARY KEY (run_id, airport_name),

        CONSTRAINT FK_GT2_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id)
    );
END;
GO


/* ============================================================
   GT3
   ============================================================ */

IF OBJECT_ID(N'bi.GT3_UK_Airport_Market_Ranking', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT3_UK_Airport_Market_Ranking (
        run_id              NVARCHAR(64)  NOT NULL,
        rank                INT           NOT NULL,
        airport_name        NVARCHAR(200) NOT NULL,
        comparison_period   INT           NOT NULL,
        passengers_current  BIGINT        NOT NULL,
        passengers_prior    BIGINT        NOT NULL,
        absolute_change     BIGINT        NOT NULL,
        market_share_pct    DECIMAL(19,8) NOT NULL,

        CONSTRAINT PK_GT3
            PRIMARY KEY (run_id, airport_name),

        CONSTRAINT UQ_GT3_Rank
            UNIQUE (run_id, rank),

        CONSTRAINT FK_GT3_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT3_Rank
            CHECK (rank >= 1),

        CONSTRAINT CK_GT3_MarketShare
            CHECK (
                market_share_pct >= 0
                AND market_share_pct <= 100
            )
    );
END;
GO


/* ============================================================
   GT4
   ============================================================ */

IF OBJECT_ID(
    N'bi.GT4_Airport_Destination_Country_Flow',
    N'U'
) IS NULL
BEGIN
    CREATE TABLE bi.GT4_Airport_Destination_Country_Flow (
        run_id                     NVARCHAR(64)  NOT NULL,
        airport_name               NVARCHAR(200) NOT NULL,
        destination_country        NVARCHAR(200) NOT NULL,
        passengers_current         BIGINT        NOT NULL,
        destination_airport_count  INT           NOT NULL,
        airport_flow_share_pct     DECIMAL(19,8) NULL,
        rank_within_airport        INT           NOT NULL,

        CONSTRAINT PK_GT4
            PRIMARY KEY (
                run_id,
                airport_name,
                destination_country
            ),

        CONSTRAINT FK_GT4_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT4_Values
            CHECK (
                passengers_current >= 0
                AND destination_airport_count >= 1
                AND rank_within_airport >= 1
                AND airport_flow_share_pct >= 0
                AND airport_flow_share_pct <= 100
            )
    );
END;
GO


/* ============================================================
   GT5
   ============================================================ */

IF OBJECT_ID(N'bi.GT5_Country_Traffic_Trends', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT5_Country_Traffic_Trends (
        run_id             NVARCHAR(64)  NOT NULL,
        region             NVARCHAR(200) NOT NULL,
        country            NVARCHAR(200) NOT NULL,
        year               SMALLINT      NOT NULL,
        passengers         BIGINT        NOT NULL,
        pct_of_total_2023  DECIMAL(19,8) NULL,
        annual_growth_pct  DECIMAL(19,6) NULL,
        passengers_2019    BIGINT        NULL,
        index_vs_2019      DECIMAL(19,6) NULL,

        CONSTRAINT PK_GT5
            PRIMARY KEY (run_id, country, year),

        CONSTRAINT FK_GT5_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT5_Year
            CHECK (year BETWEEN 1900 AND 2100),

        CONSTRAINT CK_GT5_Passengers
            CHECK (passengers >= 0)
    );
END;
GO


/* ============================================================
   GT6
   ============================================================ */

IF OBJECT_ID(N'bi.GT6_SFO_Historical_Benchmark', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT6_SFO_Historical_Benchmark (
        run_id                    NVARCHAR(64)  NOT NULL,
        year                      SMALLINT      NOT NULL,
        domestic_passengers       BIGINT        NOT NULL,
        international_passengers  BIGINT        NOT NULL,
        total_passengers          BIGINT        NOT NULL,
        classified_passengers     BIGINT        NOT NULL,
        classification_delta      BIGINT        NOT NULL,
        international_share_pct   DECIMAL(19,8) NULL,
        annual_growth_pct         DECIMAL(19,6) NULL,

        CONSTRAINT PK_GT6
            PRIMARY KEY (run_id, year),

        CONSTRAINT FK_GT6_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT6_Passengers
            CHECK (
                domestic_passengers >= 0
                AND international_passengers >= 0
                AND total_passengers >= 0
            )
    );
END;
GO


/* ============================================================
   GT7
   ============================================================ */

IF OBJECT_ID(N'bi.GT7_Global_Airport_Benchmark', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT7_Global_Airport_Benchmark (
        run_id                         NVARCHAR(64)  NOT NULL,
        source_rank                    INT           NOT NULL,
        city                           NVARCHAR(200) NOT NULL,
        airport_name                   NVARCHAR(250) NOT NULL,
        passengers_2022                BIGINT        NOT NULL,
        passengers_2021                BIGINT        NOT NULL,
        passenger_growth_pct           DECIMAL(19,6) NULL,
        aircraft_movements_2022        BIGINT        NOT NULL,
        aircraft_movements_2021        BIGINT        NOT NULL,
        aircraft_movement_growth_pct   DECIMAL(19,6) NULL,
        passengers_per_movement_2022   DECIMAL(19,6) NULL,
        passenger_scale_score          DECIMAL(19,10) NULL,
        growth_score                   DECIMAL(19,10) NULL,
        movement_scale_score           DECIMAL(19,10) NULL,
        traffic_intensity_score        DECIMAL(19,10) NULL,

        CONSTRAINT PK_GT7
            PRIMARY KEY (run_id, airport_name),

        CONSTRAINT FK_GT7_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT7_SourceRank
            CHECK (source_rank >= 1)
    );
END;
GO


/* ============================================================
   GT8
   ============================================================ */

IF OBJECT_ID(N'bi.GT8_UK_Airport_Connectivity', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT8_UK_Airport_Connectivity (
        run_id                         NVARCHAR(64)  NOT NULL,
        airport_name                   NVARCHAR(200) NOT NULL,
        passengers_current             BIGINT        NOT NULL,
        destination_country_count      INT           NOT NULL,
        destination_airport_count      INT           NOT NULL,
        scheduled_passengers           BIGINT        NOT NULL,
        charter_passengers             BIGINT        NOT NULL,
        scheduled_share_pct            DECIMAL(19,8) NULL,
        charter_share_pct              DECIMAL(19,8) NULL,
        component_reconciliation_delta BIGINT        NOT NULL,

        CONSTRAINT PK_GT8
            PRIMARY KEY (run_id, airport_name),

        CONSTRAINT FK_GT8_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT8_Counts
            CHECK (
                passengers_current >= 0
                AND destination_country_count >= 1
                AND destination_airport_count >= 1
                AND scheduled_passengers >= 0
                AND charter_passengers >= 0
            )
    );
END;
GO


/* ============================================================
   GT9
   ============================================================ */

IF OBJECT_ID(N'bi.GT9_Operational_KPI_Summary', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT9_Operational_KPI_Summary (
        run_id             NVARCHAR(64)   NOT NULL,
        generated_at_utc   DATETIME2(3)   NOT NULL,
        kpi_category       NVARCHAR(50)   NOT NULL,
        kpi_name           NVARCHAR(200)  NOT NULL,
        value_numeric      DECIMAL(38,6)  NULL,
        value_text         NVARCHAR(1000) NULL,
        unit               NVARCHAR(50)   NOT NULL,
        status             NVARCHAR(10)   NOT NULL,
        source_or_table    NVARCHAR(200)  NOT NULL,
        quality_status     NVARCHAR(10)   NOT NULL,

        CONSTRAINT PK_GT9
            PRIMARY KEY (
                run_id,
                kpi_category,
                kpi_name
            ),

        CONSTRAINT FK_GT9_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT9_Status
            CHECK (
                status IN (N'PASS', N'WARN', N'FAIL')
            ),

        CONSTRAINT CK_GT9_QualityStatus
            CHECK (
                quality_status IN (N'PASS', N'WARN', N'FAIL')
            ),

        CONSTRAINT CK_GT9_ValuePresent
            CHECK (
                value_numeric IS NOT NULL
                OR value_text IS NOT NULL
            )
    );
END;
GO


/* ============================================================
   GT10
   ============================================================ */

IF OBJECT_ID(N'bi.GT10_Decision_Recommendation', N'U') IS NULL
BEGIN
    CREATE TABLE bi.GT10_Decision_Recommendation (
        run_id                          NVARCHAR(64)  NOT NULL,
        decision_scope                  NVARCHAR(40)  NOT NULL,
        scenario                        NVARCHAR(40)  NOT NULL,
        candidate_name                  NVARCHAR(250) NOT NULL,

        raw_passengers                  BIGINT        NULL,
        raw_growth_pct                  DECIMAL(19,6) NULL,
        raw_country_breadth             INT           NULL,
        raw_route_breadth               INT           NULL,
        raw_aircraft_movements          BIGINT        NULL,
        raw_passengers_per_movement     DECIMAL(19,6) NULL,

        passenger_score                 DECIMAL(19,10) NULL,
        connectivity_score              DECIMAL(19,10) NULL,
        growth_score                    DECIMAL(19,10) NULL,
        movement_scale_score            DECIMAL(19,10) NULL,
        traffic_intensity_score         DECIMAL(19,10) NULL,
        operational_score               DECIMAL(19,10) NULL,
        growth_context                  DECIMAL(19,6) NULL,

        weight_passenger_scale          DECIMAL(19,10) NOT NULL,
        weight_country_breadth          DECIMAL(19,10) NOT NULL,
        weight_route_breadth            DECIMAL(19,10) NOT NULL,
        weight_passenger_growth         DECIMAL(19,10) NOT NULL,
        weight_movement_scale           DECIMAL(19,10) NOT NULL,
        weight_traffic_intensity        DECIMAL(19,10) NOT NULL,

        composite_score                 DECIMAL(19,10) NULL,
        rank_within_scope               INT           NULL,
        recommendation_tier             NVARCHAR(20)  NOT NULL,
        data_quality_flag               NVARCHAR(40)  NOT NULL,
        model_version                   NVARCHAR(64)  NOT NULL,

        CONSTRAINT PK_GT10
            PRIMARY KEY (
                run_id,
                decision_scope,
                scenario,
                candidate_name,
                model_version
            ),

        CONSTRAINT FK_GT10_Run
            FOREIGN KEY (run_id)
            REFERENCES meta.PipelineRun(run_id),

        CONSTRAINT CK_GT10_Scope
            CHECK (
                decision_scope IN (
                    N'UK_SITE',
                    N'GLOBAL_EXPANSION'
                )
            ),

        CONSTRAINT CK_GT10_Tier
            CHECK (
                recommendation_tier IN (
                    N'PRIMARY',
                    N'SHORTLIST',
                    N'REVIEW'
                )
            ),

        CONSTRAINT CK_GT10_Score
            CHECK (
                composite_score IS NULL
                OR (
                    composite_score >= 0
                    AND composite_score <= 1
                )
            )
    );
END;
GO


/* ============================================================
   SUPPORTING INDEXES
   ============================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = N'IX_GT4_DestinationCountry'
      AND object_id = OBJECT_ID(
          N'bi.GT4_Airport_Destination_Country_Flow'
      )
)
BEGIN
    CREATE INDEX IX_GT4_DestinationCountry
        ON bi.GT4_Airport_Destination_Country_Flow (
            run_id,
            destination_country
        );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = N'IX_GT5_Year'
      AND object_id = OBJECT_ID(
          N'bi.GT5_Country_Traffic_Trends'
      )
)
BEGIN
    CREATE INDEX IX_GT5_Year
        ON bi.GT5_Country_Traffic_Trends (
            run_id,
            year
        );
END;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = N'IX_GT10_Reporting'
      AND object_id = OBJECT_ID(
          N'bi.GT10_Decision_Recommendation'
      )
)
BEGIN
    CREATE INDEX IX_GT10_Reporting
        ON bi.GT10_Decision_Recommendation (
            run_id,
            decision_scope,
            scenario,
            rank_within_scope
        );
END;
GO
