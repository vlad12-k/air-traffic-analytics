from __future__ import annotations

import numpy as np
import pandas as pd

from airtraffic.metrics import percentile_score, safe_growth_pct


def _require_single_route_period(routes: pd.DataFrame) -> int:
    periods = (
        pd.to_numeric(routes["period"], errors="raise")
        .dropna()
        .astype(int)
        .unique()
    )

    if len(periods) != 1:
        raise ValueError(
            "ROUTES contract requires exactly one comparison snapshot; "
            f"found periods: {sorted(periods.tolist())}"
        )

    return int(periods[0])


def gt1_uk_airport_period_totals(
    routes: pd.DataFrame,
) -> pd.DataFrame:
    """GT1: observed UK airport passenger totals for the route snapshot."""
    period = _require_single_route_period(routes)

    result = (
        routes.groupby("uk_airport", as_index=False)
        .agg(
            passengers_current=("passengers_current", "sum"),
            passengers_prior=("passengers_prior", "sum"),
        )
        .rename(columns={"uk_airport": "airport_name"})
    )

    result["absolute_change"] = (
        result["passengers_current"]
        - result["passengers_prior"]
    )

    result["comparison_period"] = period

    return (
        result.sort_values(
            ["passengers_current", "airport_name"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )


def gt2_uk_airport_period_change(
    gt1: pd.DataFrame,
) -> pd.DataFrame:
    """GT2: period change with explicit zero-baseline handling."""
    result = gt1.copy()

    result["growth_pct"] = safe_growth_pct(
        result["passengers_current"],
        result["passengers_prior"],
    )

    result["zero_baseline"] = (
        result["passengers_prior"] == 0
    )

    return result.reset_index(drop=True)


def gt3_uk_airport_market_ranking(
    gt1: pd.DataFrame,
) -> pd.DataFrame:
    """GT3: full UK airport population ranked by current passenger scale."""
    result = gt1[
        [
            "airport_name",
            "comparison_period",
            "passengers_current",
            "passengers_prior",
            "absolute_change",
        ]
    ].copy()

    represented_total = float(
        result["passengers_current"].sum()
    )

    result["market_share_pct"] = np.where(
        represented_total > 0,
        result["passengers_current"].astype(float)
        / represented_total
        * 100,
        np.nan,
    )

    result = result.sort_values(
        ["passengers_current", "airport_name"],
        ascending=[False, True],
    ).reset_index(drop=True)

    result.insert(
        0,
        "rank",
        range(1, len(result) + 1),
    )

    return result


def gt4_airport_destination_country_flow(
    routes: pd.DataFrame,
) -> pd.DataFrame:
    """GT4: complete UK-airport × destination-country passenger flows."""
    _require_single_route_period(routes)

    result = (
        routes.groupby(
            ["uk_airport", "destination_country"],
            as_index=False,
        )
        .agg(
            passengers_current=("passengers_current", "sum"),
            destination_airport_count=(
                "destination_airport",
                "nunique",
            ),
        )
        .rename(columns={"uk_airport": "airport_name"})
    )

    airport_total = result.groupby(
        "airport_name"
    )["passengers_current"].transform("sum")

    result["airport_flow_share_pct"] = np.where(
        airport_total > 0,
        result["passengers_current"].astype(float)
        / airport_total.astype(float)
        * 100,
        np.nan,
    )

    result = result.sort_values(
        [
            "airport_name",
            "passengers_current",
            "destination_country",
        ],
        ascending=[True, False, True],
    ).reset_index(drop=True)

    result["rank_within_airport"] = (
        result.groupby("airport_name").cumcount() + 1
    )

    return result


def gt5_country_traffic_trends(
    avi0105: pd.DataFrame,
) -> pd.DataFrame:
    """GT5: long-term country passenger trends from AVI0105."""
    result = avi0105[
        [
            "region",
            "country",
            "year",
            "passengers",
            "pct_of_total_2023",
        ]
    ].copy()

    result = result.sort_values(
        ["country", "year"]
    ).reset_index(drop=True)

    previous_passengers = (
        result.groupby(
            "country",
            sort=False,
        )["passengers"]
        .shift(1)
        .astype(float)
    )

    current_passengers = (
        result["passengers"]
        .astype(float)
    )

    result["annual_growth_pct"] = np.where(
        previous_passengers > 0,
        (
            (
                current_passengers
                - previous_passengers
            )
            / previous_passengers
        )
        * 100,
        np.nan,
    )

    baseline = (
        result.loc[
            result["year"] == 2019,
            ["country", "passengers"],
        ]
        .rename(
            columns={
                "passengers": "passengers_2019"
            }
        )
    )

    if baseline["country"].duplicated().any():
        raise ValueError(
            "AVI0105 contract requires one 2019 baseline per country."
        )

    result = result.merge(
        baseline,
        on="country",
        how="left",
        validate="many_to_one",
    )

    result["index_vs_2019"] = np.where(
        result["passengers_2019"].astype(float) > 0,
        result["passengers"].astype(float)
        / result["passengers_2019"].astype(float)
        * 100,
        np.nan,
    )

    return result


def gt6_sfo_historical_benchmark(
    sfo: pd.DataFrame,
) -> pd.DataFrame:
    """GT6: annual SFO benchmark with domestic/international context."""
    classified = (
        sfo.groupby(
            ["year", "geo_summary"],
            as_index=False,
        )
        .agg(
            passengers=("passenger_count", "sum")
        )
    )

    pivot = (
        classified.pivot_table(
            index="year",
            columns="geo_summary",
            values="passengers",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )

    pivot.columns.name = None

    if "Domestic" not in pivot.columns:
        pivot["Domestic"] = 0

    if "International" not in pivot.columns:
        pivot["International"] = 0

    pivot = pivot.rename(
        columns={
            "Domestic": "domestic_passengers",
            "International": "international_passengers",
        }
    )

    annual_total = (
        sfo.groupby("year", as_index=False)
        .agg(
            total_passengers=(
                "passenger_count",
                "sum",
            )
        )
    )

    result = pivot.merge(
        annual_total,
        on="year",
        how="inner",
        validate="one_to_one",
    )

    result["classified_passengers"] = (
        result["domestic_passengers"]
        + result["international_passengers"]
    )

    result["classification_delta"] = (
        result["total_passengers"]
        - result["classified_passengers"]
    )

    result["international_share_pct"] = np.where(
        result["total_passengers"].astype(float) > 0,
        result["international_passengers"].astype(float)
        / result["total_passengers"].astype(float)
        * 100,
        np.nan,
    )

    result = result.sort_values(
        "year"
    ).reset_index(drop=True)

    previous_total_passengers = (
        result["total_passengers"]
        .shift(1)
        .astype(float)
    )

    current_total_passengers = (
        result["total_passengers"]
        .astype(float)
    )

    result["annual_growth_pct"] = np.where(
        previous_total_passengers > 0,
        (
            (
                current_total_passengers
                - previous_total_passengers
            )
            / previous_total_passengers
        )
        * 100,
        np.nan,
    )

    return result


def gt7_global_airport_benchmark(
    avi0301: pd.DataFrame,
) -> pd.DataFrame:
    """GT7: complete international airport benchmark population."""
    result = avi0301[
        [
            "rank",
            "city",
            "airport_name",
            "passengers_2022",
            "passengers_2021",
            "passenger_growth_pct",
            "aircraft_movements_2022",
            "aircraft_movements_2021",
            "aircraft_movement_growth_pct",
        ]
    ].copy()

    result = result.rename(
        columns={"rank": "source_rank"}
    )

    movements = result[
        "aircraft_movements_2022"
    ].astype(float)

    result["passengers_per_movement_2022"] = np.where(
        movements > 0,
        result["passengers_2022"].astype(float)
        / movements,
        np.nan,
    )

    result["passenger_scale_score"] = percentile_score(
        result["passengers_2022"]
    )

    result["growth_score"] = percentile_score(
        result["passenger_growth_pct"]
    )

    result["movement_scale_score"] = percentile_score(
        result["aircraft_movements_2022"]
    )

    result["traffic_intensity_score"] = percentile_score(
        result["passengers_per_movement_2022"]
    )

    return (
        result.sort_values(
            ["passengers_2022", "airport_name"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )


def gt8_uk_airport_connectivity(
    routes: pd.DataFrame,
) -> pd.DataFrame:
    """GT8: observed UK airport connectivity and traffic mix."""
    _require_single_route_period(routes)

    result = (
        routes.groupby(
            "uk_airport",
            as_index=False,
        )
        .agg(
            passengers_current=(
                "passengers_current",
                "sum",
            ),
            destination_country_count=(
                "destination_country",
                "nunique",
            ),
            destination_airport_count=(
                "destination_airport",
                "nunique",
            ),
            scheduled_passengers=(
                "scheduled_current",
                "sum",
            ),
            charter_passengers=(
                "charter_current",
                "sum",
            ),
        )
        .rename(
            columns={"uk_airport": "airport_name"}
        )
    )

    total = result[
        "passengers_current"
    ].astype(float)

    result["scheduled_share_pct"] = np.where(
        total > 0,
        result["scheduled_passengers"].astype(float)
        / total
        * 100,
        np.nan,
    )

    result["charter_share_pct"] = np.where(
        total > 0,
        result["charter_passengers"].astype(float)
        / total
        * 100,
        np.nan,
    )

    result["component_reconciliation_delta"] = (
        result["passengers_current"]
        - result["scheduled_passengers"]
        - result["charter_passengers"]
    )

    return (
        result.sort_values(
            ["passengers_current", "airport_name"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
    )


def build_gt1_to_gt8(
    cleaned: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """
    Build the governed analytical tables that precede quality/run metadata.

    GT9 is created after data-quality evaluation.
    GT10 is created by the decision-model layer.
    """
    gt1 = gt1_uk_airport_period_totals(
        cleaned["routes"]
    )

    gt2 = gt2_uk_airport_period_change(gt1)

    gt3 = gt3_uk_airport_market_ranking(gt1)

    gt4 = gt4_airport_destination_country_flow(
        cleaned["routes"]
    )

    gt5 = gt5_country_traffic_trends(
        cleaned["avi0105"]
    )

    gt6 = gt6_sfo_historical_benchmark(
        cleaned["sfo"]
    )

    gt7 = gt7_global_airport_benchmark(
        cleaned["avi0301"]
    )

    gt8 = gt8_uk_airport_connectivity(
        cleaned["routes"]
    )

    return {
        "GT1_UK_Airport_Period_Totals": gt1,
        "GT2_UK_Airport_Period_Change": gt2,
        "GT3_UK_Airport_Market_Ranking": gt3,
        "GT4_Airport_Destination_Country_Flow": gt4,
        "GT5_Country_Traffic_Trends": gt5,
        "GT6_SFO_Historical_Benchmark": gt6,
        "GT7_Global_Airport_Benchmark": gt7,
        "GT8_UK_Airport_Connectivity": gt8,
    }
