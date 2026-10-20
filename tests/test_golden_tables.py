import pytest

from airtraffic.clean import clean_sources
from airtraffic.golden import build_gt1_to_gt8
from airtraffic.ingest import load_sources


@pytest.fixture(scope="module")
def artifacts():
    cleaned = clean_sources(load_sources())
    tables = build_gt1_to_gt8(cleaned)
    return cleaned, tables


def test_gt1_reconciles_to_routes(artifacts):
    cleaned, tables = artifacts

    gt1 = tables["GT1_UK_Airport_Period_Totals"]

    assert gt1["airport_name"].is_unique

    assert (
        gt1["passengers_current"].sum()
        == cleaned["routes"]["passengers_current"].sum()
    )

    assert (
        gt1["passengers_prior"].sum()
        == cleaned["routes"]["passengers_prior"].sum()
    )


def test_gt3_retains_complete_population(artifacts):
    _, tables = artifacts

    gt1 = tables["GT1_UK_Airport_Period_Totals"]
    gt3 = tables["GT3_UK_Airport_Market_Ranking"]

    assert len(gt3) == len(gt1)
    assert len(gt3) > 10

    assert gt3["rank"].tolist() == list(
        range(1, len(gt3) + 1)
    )

    assert gt3["market_share_pct"].sum() == pytest.approx(
        100.0,
        abs=1e-8,
    )


def test_gt4_reconciles_to_routes(artifacts):
    cleaned, tables = artifacts

    gt4 = tables[
        "GT4_Airport_Destination_Country_Flow"
    ]

    assert (
        gt4["passengers_current"].sum()
        == cleaned["routes"]["passengers_current"].sum()
    )

    assert gt4[
        ["airport_name", "destination_country"]
    ].duplicated().sum() == 0


def test_gt5_preserves_actual_year_coverage(artifacts):
    _, tables = artifacts

    gt5 = tables["GT5_Country_Traffic_Trends"]

    assert gt5["year"].min() == 2013
    assert gt5["year"].max() == 2023

    assert "annual_growth_pct" in gt5.columns
    assert "index_vs_2019" in gt5.columns


def test_gt6_reconciles_to_sfo_source(artifacts):
    cleaned, tables = artifacts

    gt6 = tables["GT6_SFO_Historical_Benchmark"]

    assert (
        gt6["total_passengers"].sum()
        == cleaned["sfo"]["passenger_count"].sum()
    )

    assert (
        gt6["classification_delta"].abs().sum()
        == 0
    )


def test_gt7_preserves_complete_global_population(artifacts):
    cleaned, tables = artifacts

    gt7 = tables["GT7_Global_Airport_Benchmark"]

    assert len(gt7) == len(cleaned["avi0301"]) == 25

    for column in [
        "passenger_scale_score",
        "growth_score",
        "movement_scale_score",
        "traffic_intensity_score",
    ]:
        assert gt7[column].between(0, 1).all()


def test_gt8_uses_observed_connectivity_only(artifacts):
    _, tables = artifacts

    gt8 = tables["GT8_UK_Airport_Connectivity"]

    assert gt8["airport_name"].is_unique

    assert (
        gt8["destination_country_count"] >= 1
    ).all()

    assert (
        gt8["destination_airport_count"] >= 1
    ).all()

    assert (
        gt8["component_reconciliation_delta"]
        .abs()
        .sum()
        == 0
    )
