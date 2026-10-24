import pytest

from airtraffic.pipeline import (
    build_analytical_run,
)

pytestmark = pytest.mark.requires_sources


def test_analytical_run_produces_ten_governed_tables():
    run = build_analytical_run(
        run_id="TEST_PIPELINE_RUN",
        generated_at_utc=(
            "2026-10-05T00:00:00+00:00"
        ),
    )

    assert len(run.tables) == 10

    assert set(
        name.split("_", 1)[0]
        for name in run.tables
    ) == {
        f"GT{i}"
        for i in range(1, 11)
    }

    for frame in run.tables.values():
        assert "run_id" in frame.columns
        assert set(
            frame["run_id"].astype(str)
        ) == {
            "TEST_PIPELINE_RUN"
        }


def test_analytical_run_is_publishable():
    run = build_analytical_run(
        run_id="TEST_PIPELINE_RUN",
        generated_at_utc=(
            "2026-10-05T00:00:00+00:00"
        ),
    )

    blocking = run.quality_report.loc[
        (
            run.quality_report["status"]
            == "FAIL"
        )
        & (
            run.quality_report["severity"]
            == "ERROR"
        )
    ]

    assert blocking.empty
    assert not run.sensitivity_summary.empty
