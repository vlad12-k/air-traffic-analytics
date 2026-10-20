from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd

from airtraffic.config import (
    GOLDEN_DIR,
    OUTPUTS_DIR,
    QA_DIR,
)
from airtraffic.provenance import sha256_file


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        json.dump(
            payload,
            handle,
            indent=2,
            sort_keys=True,
        )


def _write_tables(
    directory: Path,
    tables: dict[str, pd.DataFrame],
) -> None:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    for old_csv in directory.glob("GT*.csv"):
        old_csv.unlink()

    for name, frame in tables.items():
        frame.to_csv(
            directory / f"{name}.csv",
            index=False,
        )


def _write_excel(
    path: Path,
    tables: dict[str, pd.DataFrame],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with pd.ExcelWriter(
        path,
        engine="openpyxl",
    ) as writer:
        for name, frame in tables.items():
            gt_id = name.split("_", 1)[0]

            frame.to_excel(
                writer,
                sheet_name=gt_id,
                index=False,
            )


def _artifact_manifest(
    run_directory: Path,
) -> dict:
    artifacts = []

    for path in sorted(
        p
        for p in run_directory.rglob("*")
        if p.is_file()
        and p.name != "artifact_manifest.json"
    ):
        artifacts.append(
            {
                "path": str(
                    path.relative_to(
                        run_directory
                    )
                ),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    return {
        "artifacts": artifacts,
    }


def export_validated_run(
    *,
    tables: dict[str, pd.DataFrame],
    quality_report: pd.DataFrame,
    sensitivity_summary: pd.DataFrame,
    eligibility_report: pd.DataFrame,
    run_context: dict,
) -> Path:
    run_id = run_context["run_id"]

    run_directory = (
        OUTPUTS_DIR
        / "runs"
        / run_id
    )

    run_golden = (
        run_directory / "golden"
    )

    run_qa = (
        run_directory / "qa"
    )

    run_golden.mkdir(
        parents=True,
        exist_ok=True,
    )

    run_qa.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Immutable run-specific evidence.
    _write_tables(
        run_golden,
        tables,
    )

    quality_report.to_csv(
        run_qa / "quality_report.csv",
        index=False,
    )

    sensitivity_summary.to_csv(
        run_qa / "gt10_sensitivity_summary.csv",
        index=False,
    )

    eligibility_report.to_csv(
        run_qa / "gt10_eligibility_report.csv",
        index=False,
    )

    _write_json(
        run_qa / "source_manifest.json",
        run_context["source_manifest"],
    )

    _write_excel(
        run_directory / "golden_tables.xlsx",
        tables,
    )

    metadata = {
        "run_id": run_id,
        "pipeline_version": run_context[
            "pipeline_version"
        ],
        "model_version": run_context[
            "model_version"
        ],
        "generated_at_utc": run_context[
            "generated_at_utc"
        ],
        "status": "VALIDATED_LOCAL",
        "source_manifest_sha256": run_context[
            "source_manifest_sha256"
        ],
        "golden_table_count": len(tables),
        "quality_check_count": len(
            quality_report
        ),
        "quality_failures": int(
            (
                quality_report["status"]
                == "FAIL"
            ).sum()
        ),
        "quality_warnings": int(
            (
                quality_report["status"]
                == "WARN"
            ).sum()
        ),
        "tables": {
            name: {
                "rows": len(frame),
                "columns": len(frame.columns),
            }
            for name, frame in tables.items()
        },
    }

    _write_json(
        run_directory / "run_metadata.json",
        metadata,
    )

    artifact_manifest = _artifact_manifest(
        run_directory
    )

    _write_json(
        run_qa / "artifact_manifest.json",
        artifact_manifest,
    )

    # Current validated outputs for easy BI consumption.
    GOLDEN_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    QA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_tables(
        GOLDEN_DIR,
        tables,
    )

    _write_excel(
        OUTPUTS_DIR / "golden_tables.xlsx",
        tables,
    )

    shutil.copy2(
        run_qa / "quality_report.csv",
        QA_DIR / "quality_report.csv",
    )

    shutil.copy2(
        run_qa / "gt10_sensitivity_summary.csv",
        QA_DIR / "gt10_sensitivity_summary.csv",
    )

    shutil.copy2(
        run_qa / "gt10_eligibility_report.csv",
        QA_DIR / "gt10_eligibility_report.csv",
    )

    shutil.copy2(
        run_qa / "source_manifest.json",
        QA_DIR / "source_manifest.json",
    )

    shutil.copy2(
        run_qa / "artifact_manifest.json",
        QA_DIR / "artifact_manifest.json",
    )

    shutil.copy2(
        run_directory / "run_metadata.json",
        QA_DIR / "run_metadata.json",
    )

    return run_directory
