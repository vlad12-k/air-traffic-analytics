from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyodbc

from airtraffic.provenance import source_manifest_sha256


TABLE_MAP = {
    "GT1_UK_Airport_Period_Totals":
        "bi.GT1_UK_Airport_Period_Totals",
    "GT2_UK_Airport_Period_Change":
        "bi.GT2_UK_Airport_Period_Change",
    "GT3_UK_Airport_Market_Ranking":
        "bi.GT3_UK_Airport_Market_Ranking",
    "GT4_Airport_Destination_Country_Flow":
        "bi.GT4_Airport_Destination_Country_Flow",
    "GT5_Country_Traffic_Trends":
        "bi.GT5_Country_Traffic_Trends",
    "GT6_SFO_Historical_Benchmark":
        "bi.GT6_SFO_Historical_Benchmark",
    "GT7_Global_Airport_Benchmark":
        "bi.GT7_Global_Airport_Benchmark",
    "GT8_UK_Airport_Connectivity":
        "bi.GT8_UK_Airport_Connectivity",
    "GT9_Operational_KPI_Summary":
        "bi.GT9_Operational_KPI_Summary",
    "GT10_Decision_Recommendation":
        "bi.GT10_Decision_Recommendation",
}


def quote_odbc(value: str) -> str:
    return "{" + value.replace("}", "}}") + "}"


def connection_string(password: str) -> str:
    required = (
        "AZURE_SQL_SERVER",
        "AZURE_SQL_DATABASE",
        "AZURE_SQL_USERNAME",
    )
    settings = {
        name: os.environ.get(name, "").strip()
        for name in required
    }
    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise ValueError(
            "Missing required Azure SQL settings: "
            + ", ".join(missing)
        )

    return ";".join(
        [
            "DRIVER={ODBC Driver 18 for SQL Server}",
            f"SERVER=tcp:{settings['AZURE_SQL_SERVER']},1433",
            f"DATABASE={settings['AZURE_SQL_DATABASE']}",
            f"UID={quote_odbc(settings['AZURE_SQL_USERNAME'])}",
            f"PWD={quote_odbc(password)}",
            "Encrypt=yes",
            "TrustServerCertificate=no",
            "Connection Timeout=60",
        ]
    )


def utc_naive(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return (
        parsed.astimezone(timezone.utc)
        .replace(tzinfo=None)
    )


def normalise_scalar(value: Any) -> Any:
    if value is None:
        return None

    if value is pd.NA:
        return None

    if isinstance(value, np.generic):
        value = value.item()

    if isinstance(value, float):
        if math.isnan(value):
            return None

    if isinstance(value, pd.Timestamp):
        if value.tzinfo is not None:
            value = (
                value.tz_convert("UTC")
                .tz_localize(None)
            )
        return value.to_pydatetime()

    try:
        missing = pd.isna(value)
        if isinstance(missing, (bool, np.bool_)):
            if bool(missing):
                return None
    except (TypeError, ValueError):
        pass

    return value


def insert_dataframe(
    cursor: pyodbc.Cursor,
    table_name: str,
    frame: pd.DataFrame,
) -> int:
    if frame.empty:
        return 0

    columns = list(frame.columns)

    column_sql = ", ".join(
        f"[{column}]"
        for column in columns
    )

    placeholders = ", ".join(
        "?"
        for _ in columns
    )

    sql = (
        f"INSERT INTO {table_name} "
        f"({column_sql}) "
        f"VALUES ({placeholders})"
    )

    rows = [
        tuple(
            normalise_scalar(value)
            for value in row
        )
        for row in frame.itertuples(
            index=False,
            name=None,
        )
    ]

    cursor.executemany(
        sql,
        rows,
    )

    return len(rows)


def verify_local_run(
    project_root: Path,
    run_id: str,
) -> tuple[
    dict,
    pd.DataFrame,
    dict[str, pd.DataFrame],
]:
    run_dir = (
        project_root
        / "outputs"
        / "runs"
        / run_id
    )

    metadata_path = (
        run_dir / "run_metadata.json"
    )

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Missing metadata: {metadata_path}"
        )

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    if metadata["run_id"] != run_id:
        raise ValueError(
            "Run ID mismatch in metadata."
        )

    if metadata["status"] != "VALIDATED_LOCAL":
        raise ValueError(
            "Only VALIDATED_LOCAL runs "
            "may be published."
        )

    if int(metadata["quality_failures"]) != 0:
        raise ValueError(
            "Local run contains quality failures."
        )

    source_manifest_path = (
        run_dir
        / "qa"
        / "source_manifest.json"
    )

    source_manifest = json.loads(
        source_manifest_path.read_text(
            encoding="utf-8"
        )
    )

    observed_manifest_hash = (
        source_manifest_sha256(
            source_manifest
        )
    )

    expected_manifest_hash = metadata[
        "source_manifest_sha256"
    ]

    if (
        observed_manifest_hash
        != expected_manifest_hash
    ):
        raise ValueError(
            "Source manifest hash mismatch."
        )

    quality_path = (
        run_dir
        / "qa"
        / "quality_report.csv"
    )

    quality = pd.read_csv(
        quality_path
    )

    if len(quality) != int(
        metadata["quality_check_count"]
    ):
        raise ValueError(
            "Quality-check count mismatch."
        )

    if set(
        quality["run_id"].astype(str)
    ) != {run_id}:
        raise ValueError(
            "Quality report run_id mismatch."
        )

    blocking = quality.loc[
        (
            quality["status"]
            == "FAIL"
        )
        & (
            quality["severity"]
            == "ERROR"
        )
    ]

    if not blocking.empty:
        raise ValueError(
            "Blocking quality failures found."
        )

    tables: dict[str, pd.DataFrame] = {}

    for logical_name in TABLE_MAP:
        path = (
            run_dir
            / "golden"
            / f"{logical_name}.csv"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Missing golden table: {path}"
            )

        frame = pd.read_csv(path)

        numeric = frame.select_dtypes(
            include=[np.number]
        )

        if not numeric.empty:
            numeric_values = numeric.to_numpy(
                dtype=float
            )

            infinite_mask = np.isinf(
                numeric_values
            )

            if infinite_mask.any():
                locations = np.argwhere(
                    infinite_mask
                )

                examples = []

                for row_index, column_index in (
                    locations[:10]
                ):
                    examples.append(
                        (
                            f"{numeric.columns[column_index]}"
                            f"@row={int(row_index)}"
                        )
                    )

                raise ValueError(
                    f"{logical_name}: found "
                    f"{int(infinite_mask.sum())} "
                    "positive/negative infinity values. "
                    "Publication stopped before Azure "
                    "transaction. Examples: "
                    + ", ".join(examples)
                )

        if set(
            frame["run_id"].astype(str)
        ) != {run_id}:
            raise ValueError(
                f"{logical_name}: run_id mismatch."
            )

        expected_rows = int(
            metadata["tables"][
                logical_name
            ]["rows"]
        )

        if len(frame) != expected_rows:
            raise ValueError(
                f"{logical_name}: expected "
                f"{expected_rows} rows, "
                f"found {len(frame)}."
            )

        if (
            logical_name
            == "GT9_Operational_KPI_Summary"
        ):
            frame["generated_at_utc"] = (
                pd.to_datetime(
                    frame[
                        "generated_at_utc"
                    ],
                    utc=True,
                )
                .dt.tz_localize(None)
            )

        tables[logical_name] = frame

    if len(tables) != 10:
        raise ValueError(
            "Expected exactly 10 golden tables."
        )

    return metadata, quality, tables


def insert_quality_checks(
    cursor: pyodbc.Cursor,
    quality: pd.DataFrame,
) -> int:
    columns = [
        "run_id",
        "check_id",
        "category",
        "object_name",
        "status",
        "severity",
        "observed_value",
        "expected_value",
        "message",
    ]

    frame = quality[columns].copy()

    for column in [
        "observed_value",
        "expected_value",
    ]:
        frame[column] = (
            frame[column]
            .where(
                frame[column].notna(),
                None,
            )
        )

    return insert_dataframe(
        cursor,
        "meta.QualityCheck",
        frame,
    )


def validate_azure_run(
    cursor: pyodbc.Cursor,
    run_id: str,
    metadata: dict,
) -> None:
    print(
        "\n===== AZURE-SIDE VALIDATION ====="
    )

    # ------------------------------------------------------
    # Exact table row counts
    # ------------------------------------------------------
    for logical_name, sql_table in (
        TABLE_MAP.items()
    ):
        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM {sql_table}
            WHERE run_id = ?;
            """,
            run_id,
        )

        actual = int(
            cursor.fetchone()[0]
        )

        expected = int(
            metadata["tables"][
                logical_name
            ]["rows"]
        )

        status = (
            "PASS"
            if actual == expected
            else "FAIL"
        )

        print(
            f"{logical_name}: "
            f"{actual}/{expected} {status}"
        )

        if actual != expected:
            raise RuntimeError(
                f"{logical_name} row-count "
                "validation failed."
            )

    # ------------------------------------------------------
    # Published quality evidence
    # ------------------------------------------------------
    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_checks,
            SUM(
                CASE
                    WHEN status = 'FAIL'
                     AND severity = 'ERROR'
                    THEN 1
                    ELSE 0
                END
            ) AS blocking_failures
        FROM meta.QualityCheck
        WHERE run_id = ?;
        """,
        run_id,
    )

    row = cursor.fetchone()

    quality_count = int(
        row.total_checks
    )

    blocking_failures = int(
        row.blocking_failures or 0
    )

    if quality_count != int(
        metadata["quality_check_count"]
    ):
        raise RuntimeError(
            "Azure quality-check count mismatch."
        )

    if blocking_failures != 0:
        raise RuntimeError(
            "Azure contains blocking "
            "quality failures."
        )

    print(
        "Quality checks:",
        quality_count,
        "PASS",
    )

    # ------------------------------------------------------
    # GT1 / GT4 / GT8 passenger reconciliation
    # ------------------------------------------------------
    cursor.execute(
        """
        SELECT
            (
                SELECT SUM(passengers_current)
                FROM bi.GT1_UK_Airport_Period_Totals
                WHERE run_id = ?
            ) AS gt1_total,

            (
                SELECT SUM(passengers_current)
                FROM bi.GT4_Airport_Destination_Country_Flow
                WHERE run_id = ?
            ) AS gt4_total,

            (
                SELECT SUM(passengers_current)
                FROM bi.GT8_UK_Airport_Connectivity
                WHERE run_id = ?
            ) AS gt8_total;
        """,
        run_id,
        run_id,
        run_id,
    )

    totals = cursor.fetchone()

    if not (
        totals.gt1_total
        == totals.gt4_total
        == totals.gt8_total
    ):
        raise RuntimeError(
            "Azure passenger reconciliation failed."
        )

    print(
        "GT1/GT4/GT8 passengers: PASS"
    )

    # ------------------------------------------------------
    # GT3 represented market = 100%
    # ------------------------------------------------------
    cursor.execute(
        """
        SELECT ABS(
            SUM(market_share_pct) - 100.0
        )
        FROM bi.GT3_UK_Airport_Market_Ranking
        WHERE run_id = ?;
        """,
        run_id,
    )

    market_delta = float(
        cursor.fetchone()[0]
    )

    if market_delta > 0.000001:
        raise RuntimeError(
            "GT3 market-share validation failed."
        )

    print("GT3 market share: PASS")

    # ------------------------------------------------------
    # GT6 classification reconciliation
    # ------------------------------------------------------
    cursor.execute(
        """
        SELECT COALESCE(
            SUM(ABS(classification_delta)),
            0
        )
        FROM bi.GT6_SFO_Historical_Benchmark
        WHERE run_id = ?;
        """,
        run_id,
    )

    if int(cursor.fetchone()[0]) != 0:
        raise RuntimeError(
            "GT6 classification "
            "reconciliation failed."
        )

    print("GT6 classification: PASS")

    # ------------------------------------------------------
    # GT8 traffic-component reconciliation
    # ------------------------------------------------------
    cursor.execute(
        """
        SELECT COALESCE(
            SUM(
                ABS(
                    component_reconciliation_delta
                )
            ),
            0
        )
        FROM bi.GT8_UK_Airport_Connectivity
        WHERE run_id = ?;
        """,
        run_id,
    )

    if int(cursor.fetchone()[0]) != 0:
        raise RuntimeError(
            "GT8 component "
            "reconciliation failed."
        )

    print("GT8 components: PASS")

    # ------------------------------------------------------
    # GT10 scoring-policy validation
    # ------------------------------------------------------
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM bi.GT10_Decision_Recommendation
        WHERE run_id = ?
          AND ABS(
                weight_passenger_scale
              + weight_country_breadth
              + weight_route_breadth
              + weight_passenger_growth
              + weight_movement_scale
              + weight_traffic_intensity
              - 1.0
          ) > 0.000000001;
        """,
        run_id,
    )

    invalid_weights = int(
        cursor.fetchone()[0]
    )

    if invalid_weights != 0:
        raise RuntimeError(
            "GT10 policy-weight validation failed."
        )

    print("GT10 policy weights: PASS")

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM bi.GT10_Decision_Recommendation
        WHERE run_id = ?
          AND data_quality_flag = 'PASS'
          AND (
                composite_score IS NULL
             OR composite_score < 0
             OR composite_score > 1
          );
        """,
        run_id,
    )

    invalid_scores = int(
        cursor.fetchone()[0]
    )

    if invalid_scores != 0:
        raise RuntimeError(
            "GT10 score-bound validation failed."
        )

    print("GT10 score bounds: PASS")

    # ------------------------------------------------------
    # One baseline PRIMARY per scope
    # ------------------------------------------------------
    cursor.execute(
        """
        SELECT
            decision_scope,
            COUNT(*) AS primary_count
        FROM bi.GT10_Decision_Recommendation
        WHERE run_id = ?
          AND scenario = 'BASELINE'
          AND recommendation_tier = 'PRIMARY'
        GROUP BY decision_scope;
        """,
        run_id,
    )

    primary_counts = {
        row.decision_scope:
            int(row.primary_count)
        for row in cursor.fetchall()
    }

    expected = {
        "UK_SITE": 1,
        "GLOBAL_EXPANSION": 1,
    }

    if primary_counts != expected:
        raise RuntimeError(
            "GT10 baseline-primary "
            f"validation failed: {primary_counts}"
        )

    print(
        "GT10 baseline PRIMARY candidates: PASS"
    )


def publish_run(
    *,
    project_root: Path,
    run_id: str,
    password: str,
) -> None:
    metadata, quality, tables = (
        verify_local_run(
            project_root,
            run_id,
        )
    )

    print(
        "===== LOCAL VALIDATED RUN ====="
    )
    print("Run ID:", run_id)
    print(
        "Pipeline version:",
        metadata["pipeline_version"],
    )
    print(
        "Model version:",
        metadata["model_version"],
    )
    print(
        "Quality checks:",
        metadata["quality_check_count"],
    )
    print(
        "Source SHA256:",
        metadata[
            "source_manifest_sha256"
        ],
    )

    conn = pyodbc.connect(
        connection_string(password),
        timeout=60,
        autocommit=False,
    )

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM meta.PipelineRun
            WHERE run_id = ?;
            """,
            run_id,
        )

        if int(cursor.fetchone()[0]) != 0:
            raise RuntimeError(
                "This run_id already exists "
                "in Azure. Publication aborted."
            )

        print(
            "\n===== BEGIN TRANSACTION ====="
        )

        cursor.execute(
            """
            INSERT INTO meta.PipelineRun (
                run_id,
                pipeline_version,
                model_version,
                started_at_utc,
                completed_at_utc,
                published_at_utc,
                publish_status,
                quality_failed_checks,
                quality_warning_checks,
                source_manifest_sha256
            )
            VALUES (
                ?, ?, ?, ?,
                NULL,
                NULL,
                'RUNNING',
                ?, ?, ?
            );
            """,
            run_id,
            metadata["pipeline_version"],
            metadata["model_version"],
            utc_naive(
                metadata["generated_at_utc"]
            ),
            int(
                metadata["quality_failures"]
            ),
            int(
                metadata["quality_warnings"]
            ),
            metadata[
                "source_manifest_sha256"
            ],
        )

        print(
            "meta.PipelineRun: RUNNING"
        )

        quality_rows = (
            insert_quality_checks(
                cursor,
                quality,
            )
        )

        print(
            "meta.QualityCheck:",
            quality_rows,
            "rows",
        )

        for logical_name, sql_table in (
            TABLE_MAP.items()
        ):
            inserted = insert_dataframe(
                cursor,
                sql_table,
                tables[logical_name],
            )

            print(
                f"{sql_table}: "
                f"{inserted} rows"
            )

        validate_azure_run(
            cursor,
            run_id,
            metadata,
        )

        cursor.execute(
            """
            UPDATE meta.PipelineRun
            SET
                publish_status = 'PUBLISHED',
                completed_at_utc =
                    SYSUTCDATETIME(),
                published_at_utc =
                    SYSUTCDATETIME()
            WHERE run_id = ?
              AND publish_status = 'RUNNING';
            """,
            run_id,
        )

        if cursor.rowcount != 1:
            raise RuntimeError(
                "Failed to transition run "
                "to PUBLISHED."
            )

        conn.commit()

        print(
            "\n===== COMMIT SUCCESS ====="
        )
        print(
            "Run status: PUBLISHED"
        )

        # Post-commit reporting verification.
        cursor.execute(
            """
            SELECT
                run_id,
                pipeline_version,
                model_version,
                published_at_utc
            FROM reporting.vw_CurrentPublishedRun;
            """
        )

        current = cursor.fetchone()

        if current is None:
            raise RuntimeError(
                "Reporting layer did not "
                "expose a published run."
            )

        if current.run_id != run_id:
            raise RuntimeError(
                "Published reporting run "
                "does not match target run."
            )

        print(
            "\n===== REPORTING LAYER ====="
        )
        print(
            "Current published run:",
            current.run_id,
        )

        cursor.execute(
            """
            SELECT
                decision_scope,
                candidate_name,
                composite_score,
                rank_within_scope,
                data_quality_flag
            FROM
                reporting.vw_GT10_Baseline_Recommendation
            WHERE recommendation_tier = 'PRIMARY'
            ORDER BY decision_scope;
            """
        )

        print(
            "\nBASELINE PRIMARY recommendations:"
        )

        for row in cursor.fetchall():
            print(
                f" - {row.decision_scope}: "
                f"{row.candidate_name} "
                f"(score={row.composite_score}, "
                f"rank={row.rank_within_scope}, "
                f"DQ={row.data_quality_flag})"
            )

    except Exception:
        conn.rollback()

        print(
            "\n===== ROLLBACK ====="
        )
        print(
            "Publication failed. "
            "No partial V2 run was committed."
        )

        raise

    finally:
        conn.close()
