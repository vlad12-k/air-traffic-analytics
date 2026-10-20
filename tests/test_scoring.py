import pytest

from airtraffic.clean import clean_sources
from airtraffic.golden import build_gt1_to_gt8
from airtraffic.ingest import load_sources
from airtraffic.scoring import (
    build_gt10_decision_recommendation,
    build_gt10_sensitivity_summary,
)


@pytest.fixture(scope="module")
def gt10():
    cleaned = clean_sources(load_sources())
    tables = build_gt1_to_gt8(cleaned)
    return build_gt10_decision_recommendation(
        tables
    )


def test_gt10_contains_two_separate_decision_scopes(gt10):
    assert set(gt10["decision_scope"]) == {
        "UK_SITE",
        "GLOBAL_EXPANSION",
    }


def test_gt10_contains_three_scenarios_per_scope(gt10):
    expected = {
        "UK_SITE": {
            "BASELINE",
            "VOLUME_HEAVY",
            "CONNECTIVITY_HEAVY",
        },
        "GLOBAL_EXPANSION": {
            "BASELINE",
            "SCALE_HEAVY",
            "GROWTH_HEAVY",
        },
    }

    for scope, scenarios in expected.items():
        observed = set(
            gt10.loc[
                gt10["decision_scope"] == scope,
                "scenario",
            ]
        )

        assert observed == scenarios


def test_gt10_has_one_candidate_record_per_scenario(gt10):
    assert not gt10.duplicated(
        [
            "decision_scope",
            "scenario",
            "candidate_name",
            "model_version",
        ]
    ).any()


def test_gt10_composite_scores_are_bounded(gt10):
    valid = gt10["composite_score"].dropna()

    assert valid.between(0, 1).all()


def test_gt10_ranks_are_sequential_within_scope_and_scenario(gt10):
    for _, frame in gt10.groupby(
        ["decision_scope", "scenario"]
    ):
        ranks = (
            frame["rank_within_scope"]
            .dropna()
            .astype(int)
            .sort_values()
            .tolist()
        )

        assert ranks == list(
            range(1, len(ranks) + 1)
        )


def test_gt10_policy_weights_sum_to_one(gt10):
    weight_columns = [
        "weight_passenger_scale",
        "weight_country_breadth",
        "weight_route_breadth",
        "weight_passenger_growth",
        "weight_movement_scale",
        "weight_traffic_intensity",
    ]

    totals = gt10[weight_columns].sum(axis=1)

    assert totals.sub(1.0).abs().le(1e-9).all()


def test_gt10_contains_no_legacy_fabricated_metrics(gt10):
    forbidden = {
        "intl_share_pct",
        "recovery_vs_2019_pct",
        "route_count",
    }

    assert forbidden.isdisjoint(gt10.columns)


def test_gt10_sensitivity_summary_is_complete(gt10):
    summary = build_gt10_sensitivity_summary(
        gt10
    )

    assert not summary.empty

    assert {
        "baseline_rank",
        "rank_min",
        "rank_max",
        "rank_range",
        "scope_top_candidate_stable",
    }.issubset(summary.columns)


def test_global_expansion_excludes_observed_uk_airports():
    from airtraffic.scoring import (
        build_gt10_eligibility_report,
    )

    cleaned = clean_sources(
        load_sources()
    )

    tables = build_gt1_to_gt8(
        cleaned
    )

    eligibility = (
        build_gt10_eligibility_report(
            tables
        )
    )

    gt10 = (
        build_gt10_decision_recommendation(
            tables
        )
    )

    excluded = set(
        eligibility.loc[
            ~eligibility[
                "eligible_for_global_expansion"
            ],
            "candidate_name",
        ]
    )

    global_candidates = set(
        gt10.loc[
            gt10[
                "decision_scope"
            ] == "GLOBAL_EXPANSION",
            "candidate_name",
        ]
    )

    assert excluded
    assert excluded.isdisjoint(
        global_candidates
    )

    assert (
        eligibility.loc[
            ~eligibility[
                "eligible_for_global_expansion"
            ],
            "eligibility_reason",
        ]
        == "EXCLUDED_UK_INITIAL_MARKET"
    ).all()
