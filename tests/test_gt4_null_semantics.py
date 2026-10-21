import pytest

from airtraffic.clean import clean_sources
from airtraffic.golden import build_gt1_to_gt8
from airtraffic.ingest import load_sources

pytestmark = pytest.mark.requires_sources


def test_gt4_flow_share_null_only_for_zero_denominator():
    raw = load_sources()
    cleaned = clean_sources(raw)
    tables = build_gt1_to_gt8(cleaned)

    gt4 = tables[
        "GT4_Airport_Destination_Country_Flow"
    ]

    airport_totals = (
        gt4.groupby("airport_name")[
            "passengers_current"
        ].transform("sum")
    )

    actual_null = gt4[
        "airport_flow_share_pct"
    ].isna()

    expected_null = airport_totals.eq(0)

    assert (
        actual_null == expected_null
    ).all()
