from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from airtraffic.clean import clean_sources
from airtraffic.export import (
    export_validated_run,
)
from airtraffic.golden import (
    build_gt1_to_gt8,
)
from airtraffic.ingest import (
    load_sources,
    source_summary,
)
from airtraffic.provenance import (
    create_run_context,
)
from airtraffic.quality import (
    assert_publishable,
    build_gt9_operational_kpi_summary,
    evaluate_quality,
)
from airtraffic.scoring import (
    build_gt10_decision_recommendation,
    build_gt10_eligibility_report,
    build_gt10_sensitivity_summary,
)


@dataclass
class AnalyticalRun:
    tables: dict[str, pd.DataFrame]
    quality_report: pd.DataFrame
    sensitivity_summary: pd.DataFrame
    eligibility_report: pd.DataFrame


def _attach_run_id(
    frame: pd.DataFrame,
    run_id: str,
) -> pd.DataFrame:
    result = frame.copy()

    if "run_id" in result.columns:
        observed = set(
            result["run_id"].astype(str)
        )

        if observed != {run_id}:
            raise ValueError(
                "Existing run_id does not match "
                "the active pipeline run."
            )

        return result

    result.insert(
        0,
        "run_id",
        run_id,
    )

    return result


def build_analytical_run(
    *,
    run_id: str,
    generated_at_utc: str,
) -> AnalyticalRun:
    raw = load_sources()
    cleaned = clean_sources(raw)

    tables = build_gt1_to_gt8(
        cleaned
    )

    gt10 = (
        build_gt10_decision_recommendation(
            tables
        )
    )

    quality_report = evaluate_quality(
        raw,
        cleaned,
        tables,
        gt10,
    )

    # Nothing reaches the publish/export layer
    # if an ERROR-level reconciliation fails.
    assert_publishable(
        quality_report
    )

    gt9 = (
        build_gt9_operational_kpi_summary(
            raw=raw,
            tables=tables,
            gt10=gt10,
            quality_report=quality_report,
            run_id=run_id,
            generated_at_utc=generated_at_utc,
        )
    )

    tables[
        "GT9_Operational_KPI_Summary"
    ] = gt9

    tables[
        "GT10_Decision_Recommendation"
    ] = gt10

    publish_tables = {
        name: _attach_run_id(
            frame,
            run_id,
        )
        for name, frame in tables.items()
    }

    quality_report = quality_report.copy()
    quality_report.insert(
        0,
        "run_id",
        run_id,
    )

    sensitivity = (
        build_gt10_sensitivity_summary(
            gt10
        )
    )

    sensitivity.insert(
        0,
        "run_id",
        run_id,
    )

    eligibility = build_gt10_eligibility_report(
        tables
    )

    eligibility.insert(
        0,
        "run_id",
        run_id,
    )

    return AnalyticalRun(
        tables=publish_tables,
        quality_report=quality_report,
        sensitivity_summary=sensitivity,
        eligibility_report=eligibility,
    )


def run_pipeline() -> AnalyticalRun:
    context = create_run_context()

    print("Air Traffic Analytics V2")
    print("=" * 72)
    print(
        f"Run ID: {context['run_id']}"
    )
    print(
        "Source manifest SHA256: "
        f"{context['source_manifest_sha256']}"
    )

    print("\n[1/7] Source ingestion")
    raw_preview = load_sources()
    print(
        source_summary(
            raw_preview
        ).to_string(index=False)
    )

    print("\n[2/7] Transformation")
    print(
        "Cleaning, normalisation and "
        "feature engineering..."
    )

    print("\n[3/7] Governed analytical layer")
    print(
        "Building GT1-GT8 and "
        "GT10 decision model..."
    )

    analytical_run = (
        build_analytical_run(
            run_id=context["run_id"],
            generated_at_utc=context[
                "generated_at_utc"
            ],
        )
    )

    print("\n[4/7] Quality and reconciliation")
    report = analytical_run.quality_report

    print(
        report[
            [
                "category",
                "status",
            ]
        ]
        .value_counts()
        .to_string()
    )

    print("\n[5/7] GT9 operational layer")
    print(
        "Operational KPI and data-quality "
        "summary created."
    )

    print("\n[6/7] Local validated publication")

    run_directory = export_validated_run(
        tables=analytical_run.tables,
        quality_report=(
            analytical_run.quality_report
        ),
        sensitivity_summary=(
            analytical_run.sensitivity_summary
        ),
        eligibility_report=(
            analytical_run.eligibility_report
        ),
        run_context=context,
    )

    print(
        f"Validated artifacts: {run_directory}"
    )

    print("\n[7/7] Strategic recommendations")

    gt10 = analytical_run.tables[
        "GT10_Decision_Recommendation"
    ]

    baseline = gt10.loc[
        (gt10["scenario"] == "BASELINE")
        & (
            gt10["rank_within_scope"]
            == 1
        ),
        [
            "decision_scope",
            "candidate_name",
            "composite_score",
            "data_quality_flag",
            "model_version",
        ],
    ]

    print("\nBASELINE winners:")
    print(
        baseline.to_string(
            index=False
        )
    )

    print("\nSensitivity:")
    sensitivity = (
        analytical_run.sensitivity_summary
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

        stable = bool(
            subset[
                "scope_top_candidate_stable"
            ].iloc[0]
        )

        print(
            f"  {scope}: "
            f"top candidate stable = {stable}"
        )

    print(
        "\nPipeline completed: "
        "VALIDATED_LOCAL"
    )

    return analytical_run


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
