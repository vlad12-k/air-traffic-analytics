from __future__ import annotations

import math

import numpy as np
import pandas as pd

from airtraffic.eligibility import (
    build_global_expansion_eligibility,
)
from airtraffic.metrics import percentile_score


MODEL_VERSION = "BI_DECISION_V2.0.0"


UK_SITE_SCENARIOS = {
    "BASELINE": {
        "passenger_scale": 0.50,
        "country_breadth": 0.30,
        "route_breadth": 0.20,
    },
    "VOLUME_HEAVY": {
        "passenger_scale": 0.65,
        "country_breadth": 0.20,
        "route_breadth": 0.15,
    },
    "CONNECTIVITY_HEAVY": {
        "passenger_scale": 0.35,
        "country_breadth": 0.35,
        "route_breadth": 0.30,
    },
}


GLOBAL_EXPANSION_SCENARIOS = {
    "BASELINE": {
        "passenger_scale": 0.50,
        "passenger_growth": 0.20,
        "movement_scale": 0.15,
        "traffic_intensity": 0.15,
    },
    "SCALE_HEAVY": {
        "passenger_scale": 0.65,
        "passenger_growth": 0.10,
        "movement_scale": 0.15,
        "traffic_intensity": 0.10,
    },
    "GROWTH_HEAVY": {
        "passenger_scale": 0.40,
        "passenger_growth": 0.35,
        "movement_scale": 0.10,
        "traffic_intensity": 0.15,
    },
}


GT10_COLUMNS = [
    "decision_scope",
    "scenario",
    "candidate_name",
    "raw_passengers",
    "raw_growth_pct",
    "raw_country_breadth",
    "raw_route_breadth",
    "raw_aircraft_movements",
    "raw_passengers_per_movement",
    "passenger_score",
    "connectivity_score",
    "growth_score",
    "movement_scale_score",
    "traffic_intensity_score",
    "operational_score",
    "growth_context",
    "weight_passenger_scale",
    "weight_country_breadth",
    "weight_route_breadth",
    "weight_passenger_growth",
    "weight_movement_scale",
    "weight_traffic_intensity",
    "composite_score",
    "rank_within_scope",
    "recommendation_tier",
    "data_quality_flag",
    "model_version",
]


def validate_policies() -> None:
    """Ensure every scenario is a valid explicit policy."""
    all_policies = {
        **{
            f"UK_SITE::{name}": weights
            for name, weights in UK_SITE_SCENARIOS.items()
        },
        **{
            f"GLOBAL_EXPANSION::{name}": weights
            for name, weights in GLOBAL_EXPANSION_SCENARIOS.items()
        },
    }

    for name, weights in all_policies.items():
        if not math.isclose(
            sum(weights.values()),
            1.0,
            abs_tol=1e-9,
        ):
            raise ValueError(
                f"Policy weights for {name} do not sum to 1.0"
            )


def _recommendation_tier(rank) -> str:
    if pd.isna(rank):
        return "REVIEW"

    rank = int(rank)

    if rank == 1:
        return "PRIMARY"

    if rank <= 3:
        return "SHORTLIST"

    return "REVIEW"


def _rank_scenario(
    frame: pd.DataFrame,
) -> pd.DataFrame:
    frame = frame.copy()

    frame["rank_within_scope"] = pd.Series(
        pd.NA,
        index=frame.index,
        dtype="Int64",
    )

    valid = frame["composite_score"].notna()

    ranks = (
        frame.loc[
            valid,
            "composite_score",
        ]
        .rank(
            method="first",
            ascending=False,
        )
        .astype("Int64")
    )

    frame.loc[
        valid,
        "rank_within_scope",
    ] = ranks

    frame["recommendation_tier"] = (
        frame["rank_within_scope"]
        .map(_recommendation_tier)
    )

    return frame


def _build_uk_scope(
    gt2: pd.DataFrame,
    gt8: pd.DataFrame,
) -> pd.DataFrame:
    base = gt8.merge(
        gt2[
            [
                "airport_name",
                "passengers_prior",
                "absolute_change",
                "growth_pct",
                "zero_baseline",
            ]
        ],
        on="airport_name",
        how="left",
        validate="one_to_one",
    )

    base["passenger_score"] = percentile_score(
        base["passengers_current"]
    )

    base["country_breadth_score"] = percentile_score(
        base["destination_country_count"]
    )

    base["route_breadth_score"] = percentile_score(
        base["destination_airport_count"]
    )

    base["connectivity_score"] = (
        base["country_breadth_score"]
        + base["route_breadth_score"]
    ) / 2

    outputs = []

    for scenario, weights in UK_SITE_SCENARIOS.items():
        frame = pd.DataFrame(
            {
                "decision_scope": "UK_SITE",
                "scenario": scenario,
                "candidate_name": base["airport_name"],
                "raw_passengers": base["passengers_current"],
                "raw_growth_pct": base["growth_pct"],
                "raw_country_breadth": base[
                    "destination_country_count"
                ],
                "raw_route_breadth": base[
                    "destination_airport_count"
                ],
                "raw_aircraft_movements": np.nan,
                "raw_passengers_per_movement": np.nan,
                "passenger_score": base["passenger_score"],
                "connectivity_score": base[
                    "connectivity_score"
                ],
                "growth_score": np.nan,
                "movement_scale_score": np.nan,
                "traffic_intensity_score": np.nan,
                "operational_score": np.nan,
                "growth_context": base["growth_pct"],
                "weight_passenger_scale": weights[
                    "passenger_scale"
                ],
                "weight_country_breadth": weights[
                    "country_breadth"
                ],
                "weight_route_breadth": weights[
                    "route_breadth"
                ],
                "weight_passenger_growth": 0.0,
                "weight_movement_scale": 0.0,
                "weight_traffic_intensity": 0.0,
            }
        )

        frame["composite_score"] = (
            weights["passenger_scale"]
            * base["passenger_score"]
            + weights["country_breadth"]
            * base["country_breadth_score"]
            + weights["route_breadth"]
            * base["route_breadth_score"]
        )

        frame["data_quality_flag"] = np.where(
            base["zero_baseline"],
            "ZERO_BASELINE_CONTEXT",
            "PASS",
        )

        frame["model_version"] = MODEL_VERSION

        outputs.append(
            _rank_scenario(frame)
        )

    return pd.concat(
        outputs,
        ignore_index=True,
    )


def _build_global_scope(
    gt7: pd.DataFrame,
    gt8: pd.DataFrame,
) -> pd.DataFrame:
    eligibility = (
        build_global_expansion_eligibility(
            gt7,
            gt8,
        )
    )

    eligible_candidates = set(
        eligibility.loc[
            eligibility[
                "eligible_for_global_expansion"
            ],
            "candidate_name",
        ]
    )

    base = gt7.loc[
        gt7["airport_name"].isin(
            eligible_candidates
        )
    ].copy()

    if base.empty:
        raise ValueError(
            "GLOBAL_EXPANSION has no eligible "
            "non-UK candidates."
        )

    base["operational_score"] = (
        base["movement_scale_score"]
        + base["traffic_intensity_score"]
    ) / 2

    scored_columns = [
        "passenger_scale_score",
        "growth_score",
        "movement_scale_score",
        "traffic_intensity_score",
    ]

    missing_component = base[
        scored_columns
    ].isna().any(axis=1)

    outputs = []

    for scenario, weights in (
        GLOBAL_EXPANSION_SCENARIOS.items()
    ):
        frame = pd.DataFrame(
            {
                "decision_scope": "GLOBAL_EXPANSION",
                "scenario": scenario,
                "candidate_name": base["airport_name"],
                "raw_passengers": base["passengers_2022"],
                "raw_growth_pct": base[
                    "passenger_growth_pct"
                ],
                "raw_country_breadth": np.nan,
                "raw_route_breadth": np.nan,
                "raw_aircraft_movements": base[
                    "aircraft_movements_2022"
                ],
                "raw_passengers_per_movement": base[
                    "passengers_per_movement_2022"
                ],
                "passenger_score": base[
                    "passenger_scale_score"
                ],
                "connectivity_score": np.nan,
                "growth_score": base["growth_score"],
                "movement_scale_score": base[
                    "movement_scale_score"
                ],
                "traffic_intensity_score": base[
                    "traffic_intensity_score"
                ],
                "operational_score": base[
                    "operational_score"
                ],
                "growth_context": base[
                    "passenger_growth_pct"
                ],
                "weight_passenger_scale": weights[
                    "passenger_scale"
                ],
                "weight_country_breadth": 0.0,
                "weight_route_breadth": 0.0,
                "weight_passenger_growth": weights[
                    "passenger_growth"
                ],
                "weight_movement_scale": weights[
                    "movement_scale"
                ],
                "weight_traffic_intensity": weights[
                    "traffic_intensity"
                ],
            }
        )

        frame["composite_score"] = (
            weights["passenger_scale"]
            * base["passenger_scale_score"]
            + weights["passenger_growth"]
            * base["growth_score"]
            + weights["movement_scale"]
            * base["movement_scale_score"]
            + weights["traffic_intensity"]
            * base["traffic_intensity_score"]
        )

        frame.loc[
            missing_component,
            "composite_score",
        ] = np.nan

        frame["data_quality_flag"] = np.where(
            missing_component,
            "MISSING_COMPONENT",
            "PASS",
        )

        frame["model_version"] = MODEL_VERSION

        outputs.append(
            _rank_scenario(frame)
        )

    return pd.concat(
        outputs,
        ignore_index=True,
    )


def build_gt10_eligibility_report(
    tables: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Return the auditable GLOBAL_EXPANSION eligibility population."""
    return build_global_expansion_eligibility(
        tables["GT7_Global_Airport_Benchmark"],
        tables["GT8_UK_Airport_Connectivity"],
    )


def build_gt10_decision_recommendation(
    tables: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Build both strategic decision scopes and all sensitivity scenarios."""
    validate_policies()

    uk = _build_uk_scope(
        tables["GT2_UK_Airport_Period_Change"],
        tables["GT8_UK_Airport_Connectivity"],
    )

    global_expansion = _build_global_scope(
        tables["GT7_Global_Airport_Benchmark"],
        tables["GT8_UK_Airport_Connectivity"],
    )

    result = pd.DataFrame.from_records(
        [
            *uk.to_dict(orient="records"),
            *global_expansion.to_dict(orient="records"),
        ],
        columns=GT10_COLUMNS,
    )

    return (
        result[GT10_COLUMNS]
        .sort_values(
            [
                "decision_scope",
                "scenario",
                "rank_within_scope",
                "candidate_name",
            ],
            na_position="last",
        )
        .reset_index(drop=True)
    )


def build_gt10_sensitivity_summary(
    gt10: pd.DataFrame,
) -> pd.DataFrame:
    """Summarise rank stability across policy scenarios."""
    valid = gt10.loc[
        gt10["rank_within_scope"].notna()
    ].copy()

    summary = (
        valid.groupby(
            [
                "decision_scope",
                "candidate_name",
            ],
            as_index=False,
        )
        .agg(
            rank_min=(
                "rank_within_scope",
                "min",
            ),
            rank_max=(
                "rank_within_scope",
                "max",
            ),
            scenario_count=(
                "scenario",
                "nunique",
            ),
            top_scenario_count=(
                "rank_within_scope",
                lambda values: int(
                    (values == 1).sum()
                ),
            ),
        )
    )

    baseline = (
        valid.loc[
            valid["scenario"] == "BASELINE",
            [
                "decision_scope",
                "candidate_name",
                "rank_within_scope",
            ],
        ]
        .rename(
            columns={
                "rank_within_scope": "baseline_rank"
            }
        )
    )

    summary = summary.merge(
        baseline,
        on=[
            "decision_scope",
            "candidate_name",
        ],
        how="left",
        validate="one_to_one",
    )

    summary["rank_range"] = (
        summary["rank_max"]
        - summary["rank_min"]
    )

    stability = {}

    for scope, scope_frame in valid.groupby(
        "decision_scope"
    ):
        winners = (
            scope_frame.loc[
                scope_frame["rank_within_scope"] == 1,
                "candidate_name",
            ]
            .dropna()
            .unique()
        )

        stability[scope] = len(winners) == 1

    summary["scope_top_candidate_stable"] = (
        summary["decision_scope"]
        .map(stability)
    )

    return (
        summary.sort_values(
            [
                "decision_scope",
                "baseline_rank",
                "candidate_name",
            ]
        )
        .reset_index(drop=True)
    )
