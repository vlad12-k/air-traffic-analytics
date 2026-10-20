import numpy as np

from airtraffic.clean import clean_sources
from airtraffic.golden import build_gt1_to_gt8
from airtraffic.ingest import load_sources
from airtraffic.pipeline import build_analytical_run


def test_gt5_zero_previous_year_growth_is_null():
    raw = load_sources()
    cleaned = clean_sources(raw)
    tables = build_gt1_to_gt8(cleaned)

    gt5 = (
        tables[
            "GT5_Country_Traffic_Trends"
        ]
        .sort_values(
            ["country", "year"]
        )
        .reset_index(drop=True)
    )

    previous = (
        gt5.groupby(
            "country",
            sort=False,
        )["passengers"]
        .shift(1)
    )

    zero_denominator = previous.eq(0)

    assert zero_denominator.any()

    assert gt5.loc[
        zero_denominator,
        "annual_growth_pct",
    ].isna().all()


def test_governed_tables_have_no_infinite_numeric_values():
    run = build_analytical_run(
        run_id="TEST_NUMERIC_FINITE",
        generated_at_utc=(
            "2026-10-05T00:00:00+00:00"
        ),
    )

    for name, frame in run.tables.items():
        numeric = frame.select_dtypes(
            include=[np.number]
        )

        if numeric.empty:
            continue

        values = numeric.to_numpy(
            dtype=float
        )

        assert not np.isinf(values).any(), (
            f"{name} contains +/- infinity"
        )
