import pytest

from airtraffic.clean import clean_sources
from airtraffic.golden import build_gt1_to_gt8
from airtraffic.ingest import load_sources
from airtraffic.quality import (
    assert_publishable,
    build_gt9_operational_kpi_summary,
    evaluate_quality,
)
from airtraffic.scoring import (
    build_gt10_decision_recommendation,
)


@pytest.fixture(scope="module")
def artifacts():
    raw = load_sources()
    cleaned = clean_sources(raw)
    tables = build_gt1_to_gt8(cleaned)

    gt10 = build_gt10_decision_recommendation(
        tables
    )

    report = evaluate_quality(
        raw,
        cleaned,
        tables,
        gt10,
    )

    gt9 = build_gt9_operational_kpi_summary(
        raw=raw,
        tables=tables,
        gt10=gt10,
        quality_report=report,
        run_id="TEST_RUN_001",
        generated_at_utc="2026-10-05T00:00:00+00:00",
    )

    return raw, cleaned, tables, gt10, report, gt9


def test_quality_report_has_no_blocking_failures(artifacts):
    _, _, _, _, report, _ = artifacts

    failures = report.loc[
        report["status"] == "FAIL"
    ]

    assert failures.empty
    assert_publishable(report)


def test_quality_report_contains_core_reconciliations(artifacts):
    _, _, _, _, report, _ = artifacts

    required = {
        "REC_GT1_CURRENT_PASSENGERS",
        "REC_GT4_CURRENT_PASSENGERS",
        "REC_GT6_SFO_PASSENGERS",
        "REC_GT8_TRAFFIC_COMPONENTS",
        "DM_GT10_WEIGHT_POLICY",
        "DM_GT10_BASELINE_PRIMARY",
        "DM_GT10_GLOBAL_ELIGIBILITY",
    }

    assert required.issubset(
        set(report["check_id"])
    )


def test_gt9_has_market_grade_contract(artifacts):
    _, _, _, _, _, gt9 = artifacts

    required_columns = {
        "run_id",
        "generated_at_utc",
        "kpi_category",
        "kpi_name",
        "value_numeric",
        "value_text",
        "unit",
        "status",
        "source_or_table",
        "quality_status",
    }

    assert required_columns.issubset(
        gt9.columns
    )

    assert {
        "BUSINESS",
        "DATA_QUALITY",
        "PIPELINE",
        "COVERAGE",
    }.issubset(
        set(gt9["kpi_category"])
    )


def test_gt9_contains_both_baseline_recommendations(artifacts):
    _, _, _, _, _, gt9 = artifacts

    recommendation_rows = gt9.loc[
        gt9["kpi_name"].isin(
            [
                "UK_SITE baseline recommendation",
                "GLOBAL_EXPANSION baseline recommendation",
            ]
        )
    ]

    assert len(recommendation_rows) == 2
    assert recommendation_rows[
        "value_text"
    ].notna().all()


def test_publish_gate_rejects_broken_reconciliation(artifacts):
    raw, cleaned, tables, gt10, _, _ = artifacts

    broken_tables = dict(tables)

    broken_gt8 = tables[
        "GT8_UK_Airport_Connectivity"
    ].copy()

    broken_gt8.loc[
        broken_gt8.index[0],
        "component_reconciliation_delta",
    ] += 1

    broken_tables[
        "GT8_UK_Airport_Connectivity"
    ] = broken_gt8

    report = evaluate_quality(
        raw,
        cleaned,
        broken_tables,
        gt10,
    )

    assert (
        report.loc[
            report[
                "check_id"
            ] == "REC_GT8_TRAFFIC_COMPONENTS",
            "status",
        ].iloc[0]
        == "FAIL"
    )

    with pytest.raises(
        ValueError,
        match="Publish gate failed",
    ):
        assert_publishable(report)
