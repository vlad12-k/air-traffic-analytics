from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from airtraffic.scoring import (
    build_gt10_eligibility_report,
    build_gt10_sensitivity_summary,
)


EXPECTED_SOURCE_ROWS = {
    "avi0105": 77,
    "avi0301": 25,
    "sfo": 31339,
    "routes": 1752,
}


def _quality_row(
    check_id: str,
    category: str,
    object_name: str,
    status: str,
    observed_value: Any,
    expected_value: Any,
    severity: str,
    message: str,
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "category": category,
        "object_name": object_name,
        "status": status,
        "severity": severity,
        "observed_value": observed_value,
        "expected_value": expected_value,
        "message": message,
    }


def evaluate_quality(
    raw: dict[str, pd.DataFrame],
    cleaned: dict[str, pd.DataFrame],
    tables: dict[str, pd.DataFrame],
    gt10: pd.DataFrame,
) -> pd.DataFrame:
    """
    Run publish-gate checks across source, transformation,
    golden-table, reconciliation, and decision-model layers.
    """
    rows: list[dict[str, Any]] = []

    # ---------------------------------------------------------
    # Source checks
    # ---------------------------------------------------------
    for source_name, expected_rows in EXPECTED_SOURCE_ROWS.items():
        present = source_name in raw

        rows.append(
            _quality_row(
                check_id=f"SRC_{source_name.upper()}_PRESENT",
                category="SOURCE",
                object_name=source_name,
                status="PASS" if present else "FAIL",
                observed_value=present,
                expected_value=True,
                severity="ERROR",
                message="Canonical source dataset is available.",
            )
        )

        if not present:
            continue

        observed_rows = len(raw[source_name])

        rows.append(
            _quality_row(
                check_id=f"SRC_{source_name.upper()}_ROW_COUNT",
                category="SOURCE",
                object_name=source_name,
                status=(
                    "PASS"
                    if observed_rows == expected_rows
                    else "WARN"
                ),
                observed_value=observed_rows,
                expected_value=expected_rows,
                severity="WARNING",
                message=(
                    "Row count compared with the validated project snapshot. "
                    "A changed count requires source-version review but is not "
                    "automatically a publish failure."
                ),
            )
        )

        duplicate_rows = int(
            raw[source_name].duplicated().sum()
        )

        rows.append(
            _quality_row(
                check_id=f"SRC_{source_name.upper()}_DUPLICATES",
                category="SOURCE",
                object_name=source_name,
                status="PASS" if duplicate_rows == 0 else "FAIL",
                observed_value=duplicate_rows,
                expected_value=0,
                severity="ERROR",
                message="Exact duplicate source rows must not be present.",
            )
        )

    # ---------------------------------------------------------
    # Transformation checks
    # ---------------------------------------------------------
    routes_raw_rows = len(raw["routes"])
    routes_clean_rows = len(cleaned["routes"])

    rows.append(
        _quality_row(
            check_id="TRN_ROUTES_ROW_PRESERVATION",
            category="TRANSFORMATION",
            object_name="routes",
            status=(
                "PASS"
                if routes_raw_rows == routes_clean_rows
                else "FAIL"
            ),
            observed_value=routes_clean_rows,
            expected_value=routes_raw_rows,
            severity="ERROR",
            message="Route cleaning must preserve valid source records.",
        )
    )

    governed_numeric_frames = {
        **tables,
        "GT10_Decision_Recommendation": gt10,
    }

    infinite_value_count = 0

    for frame in governed_numeric_frames.values():
        numeric = frame.select_dtypes(
            include=[np.number]
        )

        for column in numeric.columns:
            values = pd.to_numeric(
                numeric[column],
                errors="coerce",
            ).to_numpy(dtype=float)

            infinite_value_count += int(
                np.isinf(values).sum()
            )

    rows.append(
        _quality_row(
            "TRN_GOVERNED_NUMERIC_FINITE",
            "TRANSFORMATION",
            "GT1-GT10",
            (
                "PASS"
                if infinite_value_count == 0
                else "FAIL"
            ),
            infinite_value_count,
            0,
            "ERROR",
            (
                "Governed analytical tables must not "
                "contain positive or negative infinity. "
                "Undefined ratios must be represented "
                "as NULL/NaN."
            ),
        )
    )

    # ---------------------------------------------------------
    # Golden-table reconciliation
    # ---------------------------------------------------------
    gt1 = tables["GT1_UK_Airport_Period_Totals"]
    gt3 = tables["GT3_UK_Airport_Market_Ranking"]
    gt4 = tables[
        "GT4_Airport_Destination_Country_Flow"
    ]
    gt6 = tables["GT6_SFO_Historical_Benchmark"]
    gt8 = tables["GT8_UK_Airport_Connectivity"]

    source_current = int(
        cleaned["routes"]["passengers_current"].sum()
    )
    source_prior = int(
        cleaned["routes"]["passengers_prior"].sum()
    )

    gt1_current = int(
        gt1["passengers_current"].sum()
    )
    gt1_prior = int(
        gt1["passengers_prior"].sum()
    )

    rows.append(
        _quality_row(
            "REC_GT1_CURRENT_PASSENGERS",
            "RECONCILIATION",
            "GT1",
            "PASS" if gt1_current == source_current else "FAIL",
            gt1_current,
            source_current,
            "ERROR",
            "GT1 current passenger total must reconcile to ROUTES.",
        )
    )

    rows.append(
        _quality_row(
            "REC_GT1_PRIOR_PASSENGERS",
            "RECONCILIATION",
            "GT1",
            "PASS" if gt1_prior == source_prior else "FAIL",
            gt1_prior,
            source_prior,
            "ERROR",
            "GT1 prior passenger total must reconcile to ROUTES.",
        )
    )

    rows.append(
        _quality_row(
            "REC_GT3_POPULATION",
            "RECONCILIATION",
            "GT3",
            "PASS" if len(gt3) == len(gt1) else "FAIL",
            len(gt3),
            len(gt1),
            "ERROR",
            "GT3 must retain the complete UK airport population.",
        )
    )

    gt3_share = float(
        gt3["market_share_pct"].sum()
    )

    rows.append(
        _quality_row(
            "REC_GT3_MARKET_SHARE",
            "RECONCILIATION",
            "GT3",
            "PASS"
            if np.isclose(gt3_share, 100.0, atol=1e-8)
            else "FAIL",
            gt3_share,
            100.0,
            "ERROR",
            "GT3 represented-market share must sum to 100%.",
        )
    )

    gt4_current = int(
        gt4["passengers_current"].sum()
    )

    rows.append(
        _quality_row(
            "REC_GT4_CURRENT_PASSENGERS",
            "RECONCILIATION",
            "GT4",
            "PASS" if gt4_current == source_current else "FAIL",
            gt4_current,
            source_current,
            "ERROR",
            "GT4 flow totals must reconcile to ROUTES.",
        )
    )

    gt4_airport_totals = (
        gt4.groupby("airport_name")[
            "passengers_current"
        ].transform("sum")
    )

    gt4_share_null_violations = int(
        (
            gt4[
                "airport_flow_share_pct"
            ].isna()
            != gt4_airport_totals.eq(0)
        ).sum()
    )

    rows.append(
        _quality_row(
            "REC_GT4_FLOW_SHARE_NULL_SEMANTICS",
            "RECONCILIATION",
            "GT4",
            (
                "PASS"
                if gt4_share_null_violations == 0
                else "FAIL"
            ),
            gt4_share_null_violations,
            0,
            "ERROR",
            (
                "GT4 airport flow share must be NULL "
                "only when the airport current-period "
                "passenger denominator is zero."
            ),
        )
    )

    sfo_source_total = int(
        cleaned["sfo"]["passenger_count"].sum()
    )

    sfo_gt6_total = int(
        gt6["total_passengers"].sum()
    )

    rows.append(
        _quality_row(
            "REC_GT6_SFO_PASSENGERS",
            "RECONCILIATION",
            "GT6",
            "PASS"
            if sfo_source_total == sfo_gt6_total
            else "FAIL",
            sfo_gt6_total,
            sfo_source_total,
            "ERROR",
            "GT6 total passengers must reconcile to the SFO source.",
        )
    )

    classification_delta = int(
        gt6["classification_delta"].abs().sum()
    )

    rows.append(
        _quality_row(
            "REC_GT6_CLASSIFICATION",
            "RECONCILIATION",
            "GT6",
            "PASS" if classification_delta == 0 else "FAIL",
            classification_delta,
            0,
            "ERROR",
            "Domestic and international classifications must reconcile.",
        )
    )

    gt8_current = int(
        gt8["passengers_current"].sum()
    )

    rows.append(
        _quality_row(
            "REC_GT8_CURRENT_PASSENGERS",
            "RECONCILIATION",
            "GT8",
            "PASS" if gt8_current == source_current else "FAIL",
            gt8_current,
            source_current,
            "ERROR",
            "GT8 passenger totals must reconcile to ROUTES.",
        )
    )

    component_delta = int(
        gt8[
            "component_reconciliation_delta"
        ].abs().sum()
    )

    rows.append(
        _quality_row(
            "REC_GT8_TRAFFIC_COMPONENTS",
            "RECONCILIATION",
            "GT8",
            "PASS" if component_delta == 0 else "FAIL",
            component_delta,
            0,
            "ERROR",
            "Scheduled + charter passengers must reconcile to totals.",
        )
    )

    # ---------------------------------------------------------
    # Decision-model governance checks
    # ---------------------------------------------------------
    expected_scopes = {
        "UK_SITE",
        "GLOBAL_EXPANSION",
    }

    observed_scopes = set(
        gt10["decision_scope"]
    )

    rows.append(
        _quality_row(
            "DM_GT10_SCOPES",
            "DECISION_MODEL",
            "GT10",
            "PASS"
            if observed_scopes == expected_scopes
            else "FAIL",
            sorted(observed_scopes),
            sorted(expected_scopes),
            "ERROR",
            "UK and global decisions must remain separate populations.",
        )
    )

    eligibility = build_gt10_eligibility_report(
        tables
    )

    excluded_candidates = set(
        eligibility.loc[
            ~eligibility[
                "eligible_for_global_expansion"
            ],
            "candidate_name",
        ]
    )

    global_candidates = set(
        gt10.loc[
            gt10["decision_scope"]
            == "GLOBAL_EXPANSION",
            "candidate_name",
        ]
    )

    leaked_candidates = sorted(
        excluded_candidates
        & global_candidates
    )

    rows.append(
        _quality_row(
            "DM_GT10_GLOBAL_ELIGIBILITY",
            "DECISION_MODEL",
            "GT10",
            "PASS"
            if not leaked_candidates
            else "FAIL",
            leaked_candidates,
            [],
            "ERROR",
            (
                "Candidates excluded from the second-stage "
                "GLOBAL_EXPANSION population must not appear "
                "in that decision scope."
            ),
        )
    )

    duplicate_grain = int(
        gt10.duplicated(
            [
                "decision_scope",
                "scenario",
                "candidate_name",
                "model_version",
            ]
        ).sum()
    )

    rows.append(
        _quality_row(
            "DM_GT10_GRAIN_UNIQUENESS",
            "DECISION_MODEL",
            "GT10",
            "PASS" if duplicate_grain == 0 else "FAIL",
            duplicate_grain,
            0,
            "ERROR",
            "GT10 analytical grain must be unique.",
        )
    )

    weight_columns = [
        "weight_passenger_scale",
        "weight_country_breadth",
        "weight_route_breadth",
        "weight_passenger_growth",
        "weight_movement_scale",
        "weight_traffic_intensity",
    ]

    weight_totals = gt10[
        weight_columns
    ].sum(axis=1)

    invalid_weight_rows = int(
        (~np.isclose(
            weight_totals.to_numpy(dtype=float),
            1.0,
            atol=1e-9,
        )).sum()
    )

    rows.append(
        _quality_row(
            "DM_GT10_WEIGHT_POLICY",
            "DECISION_MODEL",
            "GT10",
            "PASS"
            if invalid_weight_rows == 0
            else "FAIL",
            invalid_weight_rows,
            0,
            "ERROR",
            "Every scoring policy must sum to exactly 1.0.",
        )
    )

    pass_candidates = gt10.loc[
        gt10["data_quality_flag"] == "PASS"
    ]

    invalid_scores = int(
        (
            pass_candidates["composite_score"].isna()
            | ~pass_candidates[
                "composite_score"
            ].between(0, 1)
        ).sum()
    )

    rows.append(
        _quality_row(
            "DM_GT10_SCORE_BOUNDS",
            "DECISION_MODEL",
            "GT10",
            "PASS"
            if invalid_scores == 0
            else "FAIL",
            invalid_scores,
            0,
            "ERROR",
            "Publishable decision scores must be present and within 0–1.",
        )
    )

    baseline = gt10.loc[
        gt10["scenario"] == "BASELINE"
    ]

    primary_counts = (
        baseline.loc[
            baseline[
                "recommendation_tier"
            ] == "PRIMARY"
        ]
        .groupby("decision_scope")
        .size()
        .to_dict()
    )

    valid_primary_counts = all(
        primary_counts.get(scope, 0) == 1
        for scope in expected_scopes
    )

    rows.append(
        _quality_row(
            "DM_GT10_BASELINE_PRIMARY",
            "DECISION_MODEL",
            "GT10",
            "PASS"
            if valid_primary_counts
            else "FAIL",
            primary_counts,
            {
                "UK_SITE": 1,
                "GLOBAL_EXPANSION": 1,
            },
            "ERROR",
            "Each BASELINE decision scope must produce one PRIMARY candidate.",
        )
    )

    return (
        pd.DataFrame(rows)
        .sort_values(
            ["category", "check_id"]
        )
        .reset_index(drop=True)
    )


def assert_publishable(
    quality_report: pd.DataFrame,
) -> None:
    """Block publication when an ERROR-level quality gate fails."""
    failures = quality_report.loc[
        (quality_report["status"] == "FAIL")
        & (quality_report["severity"] == "ERROR")
    ]

    if failures.empty:
        return

    detail = "\n".join(
        f"- {row.check_id}: {row.message}"
        for row in failures.itertuples()
    )

    raise ValueError(
        "Publish gate failed:\n"
        + detail
    )


def build_gt9_operational_kpi_summary(
    raw: dict[str, pd.DataFrame],
    tables: dict[str, pd.DataFrame],
    gt10: pd.DataFrame,
    quality_report: pd.DataFrame,
    run_id: str,
    generated_at_utc: str,
) -> pd.DataFrame:
    """Build the operational KPI and data-quality summary for one run."""
    rows: list[dict[str, Any]] = []

    def add_numeric(
        category: str,
        name: str,
        value: float | int,
        unit: str,
        source: str,
        status: str = "PASS",
    ) -> None:
        rows.append(
            {
                "run_id": run_id,
                "generated_at_utc": generated_at_utc,
                "kpi_category": category,
                "kpi_name": name,
                "value_numeric": value,
                "value_text": pd.NA,
                "unit": unit,
                "status": status,
                "source_or_table": source,
                "quality_status": status,
            }
        )

    def add_text(
        category: str,
        name: str,
        value: str,
        unit: str,
        source: str,
        status: str = "PASS",
    ) -> None:
        rows.append(
            {
                "run_id": run_id,
                "generated_at_utc": generated_at_utc,
                "kpi_category": category,
                "kpi_name": name,
                "value_numeric": np.nan,
                "value_text": value,
                "unit": unit,
                "status": status,
                "source_or_table": source,
                "quality_status": status,
            }
        )

    gt1 = tables["GT1_UK_Airport_Period_Totals"]
    gt4 = tables[
        "GT4_Airport_Destination_Country_Flow"
    ]
    gt7 = tables["GT7_Global_Airport_Benchmark"]

    add_numeric(
        "BUSINESS",
        "Current-period international passengers",
        int(gt1["passengers_current"].sum()),
        "passengers",
        "GT1",
    )

    add_numeric(
        "BUSINESS",
        "UK airport candidates",
        int(gt1["airport_name"].nunique()),
        "airports",
        "GT1",
    )

    add_numeric(
        "BUSINESS",
        "Destination countries represented",
        int(
            gt4[
                "destination_country"
            ].nunique()
        ),
        "countries",
        "GT4",
    )

    add_numeric(
        "BUSINESS",
        "Global airport benchmark candidates",
        len(gt7),
        "airports",
        "GT7",
    )

    baseline = gt10.loc[
        (gt10["scenario"] == "BASELINE")
        & (
            gt10["recommendation_tier"]
            == "PRIMARY"
        )
    ]

    for scope in [
        "UK_SITE",
        "GLOBAL_EXPANSION",
    ]:
        winner = baseline.loc[
            baseline["decision_scope"] == scope
        ]

        if len(winner) == 1:
            add_text(
                "BUSINESS",
                f"{scope} baseline recommendation",
                str(
                    winner.iloc[0][
                        "candidate_name"
                    ]
                ),
                "candidate",
                "GT10",
            )

    sensitivity = (
        build_gt10_sensitivity_summary(
            gt10
        )
    )

    for scope in [
        "UK_SITE",
        "GLOBAL_EXPANSION",
    ]:
        subset = sensitivity.loc[
            sensitivity[
                "decision_scope"
            ] == scope
        ]

        if not subset.empty:
            stable = bool(
                subset[
                    "scope_top_candidate_stable"
                ].iloc[0]
            )

            add_numeric(
                "BUSINESS",
                f"{scope} top-candidate stability",
                int(stable),
                "boolean",
                "GT10 sensitivity",
                "PASS" if stable else "WARN",
            )

    for source_name, frame in raw.items():
        add_numeric(
            "COVERAGE",
            f"{source_name} source rows",
            len(frame),
            "rows",
            source_name,
        )

    total_checks = len(quality_report)
    failed_checks = int(
        (
            quality_report["status"]
            == "FAIL"
        ).sum()
    )
    warning_checks = int(
        (
            quality_report["status"]
            == "WARN"
        ).sum()
    )

    add_numeric(
        "DATA_QUALITY",
        "Quality checks executed",
        total_checks,
        "checks",
        "quality_report",
    )

    add_numeric(
        "DATA_QUALITY",
        "Failed quality checks",
        failed_checks,
        "checks",
        "quality_report",
        "PASS" if failed_checks == 0 else "FAIL",
    )

    add_numeric(
        "DATA_QUALITY",
        "Quality warnings",
        warning_checks,
        "checks",
        "quality_report",
        "PASS" if warning_checks == 0 else "WARN",
    )

    blocking_failures = int(
        (
            (quality_report["status"] == "FAIL")
            & (
                quality_report["severity"]
                == "ERROR"
            )
        ).sum()
    )

    add_numeric(
        "PIPELINE",
        "Publish ready",
        int(blocking_failures == 0),
        "boolean",
        "quality_report",
        "PASS"
        if blocking_failures == 0
        else "FAIL",
    )

    add_numeric(
        "PIPELINE",
        "Governed golden tables",
        10,
        "tables",
        "GT1-GT10",
    )

    return pd.DataFrame(rows)
