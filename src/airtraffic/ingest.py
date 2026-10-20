from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from airtraffic.config import SOURCE_FILES


def detect_delimiter(path: Path) -> str:
    """Detect the delimiter used by a CSV file."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(8192)

    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


def read_csv(path: Path) -> pd.DataFrame:
    """Read one source CSV using its detected delimiter."""
    if not path.exists():
        raise FileNotFoundError(f"Source dataset not found: {path}")

    return pd.read_csv(
        path,
        encoding="utf-8-sig",
        sep=detect_delimiter(path),
        engine="python",
        thousands=",",
        keep_default_na=True,
    )


def load_sources() -> dict[str, pd.DataFrame]:
    """Load all canonical source datasets."""
    return {
        name: read_csv(path)
        for name, path in SOURCE_FILES.items()
    }


def source_summary(
    datasets: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Return basic ingestion metadata for loaded datasets."""
    rows = []

    for name, frame in datasets.items():
        rows.append(
            {
                "dataset": name,
                "rows": len(frame),
                "columns": len(frame.columns),
            }
        )

    return pd.DataFrame(rows).sort_values("dataset").reset_index(drop=True)
