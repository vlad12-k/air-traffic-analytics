from __future__ import annotations

import numpy as np
import pandas as pd


def percentile_score(series: pd.Series) -> pd.Series:
    """Return a 0–1 within-population percentile score."""
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.rank(
        method="average",
        pct=True,
    )


def safe_growth_pct(
    current: pd.Series,
    prior: pd.Series,
) -> pd.Series:
    """
    Calculate percentage change only where the prior denominator is positive.

    Zero baselines remain undefined rather than being converted to an
    artificial growth value.
    """
    current_numeric = pd.to_numeric(current, errors="coerce").astype(float)
    prior_numeric = pd.to_numeric(prior, errors="coerce").astype(float)

    return pd.Series(
        np.where(
            prior_numeric > 0,
            ((current_numeric - prior_numeric) / prior_numeric) * 100,
            np.nan,
        ),
        index=current.index,
        dtype="float64",
    )
