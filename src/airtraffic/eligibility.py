from __future__ import annotations

import re
import unicodedata

import pandas as pd


def canonical_airport_name(value: str) -> str:
    """
    Produce a conservative comparison key for cross-source airport matching.

    This is used only for candidate eligibility, not as a replacement for
    the original source labels.
    """
    text = unicodedata.normalize(
        "NFKD",
        str(value),
    )

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    text = text.upper()

    text = re.sub(
        r"[^A-Z0-9]+",
        " ",
        text,
    )

    tokens = [
        token
        for token in text.split()
        if token != "AIRPORT"
    ]

    return " ".join(tokens)


def match_observed_uk_airport(
    candidate_name: str,
    uk_airports: list[str],
) -> str | None:
    """
    Match an AVI0301 airport against the observed UK airport population.

    Exact canonical matches are preferred. A suffix comparison handles
    labels such as 'London Heathrow Airport' versus 'HEATHROW'.
    """
    candidate_key = canonical_airport_name(
        candidate_name
    )

    for uk_airport in uk_airports:
        uk_key = canonical_airport_name(
            uk_airport
        )

        if not uk_key:
            continue

        if candidate_key == uk_key:
            return uk_airport

        if candidate_key.endswith(
            f" {uk_key}"
        ):
            return uk_airport

        if uk_key.endswith(
            f" {candidate_key}"
        ):
            return uk_airport

    return None


def build_global_expansion_eligibility(
    gt7: pd.DataFrame,
    gt8: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create an auditable eligibility decision for the global expansion scope.

    UK airports observed in the UK_SITE population are excluded because
    GLOBAL_EXPANSION represents the subsequent non-UK expansion decision.
    """
    uk_airports = (
        gt8["airport_name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    rows = []

    for row in gt7.itertuples():
        matched_uk_airport = (
            match_observed_uk_airport(
                row.airport_name,
                uk_airports,
            )
        )

        eligible = (
            matched_uk_airport is None
        )

        rows.append(
            {
                "candidate_name": row.airport_name,
                "source_city": row.city,
                "eligible_for_global_expansion": eligible,
                "eligibility_reason": (
                    "ELIGIBLE_NON_UK_CANDIDATE"
                    if eligible
                    else "EXCLUDED_UK_INITIAL_MARKET"
                ),
                "matched_uk_airport": (
                    matched_uk_airport
                    if matched_uk_airport
                    is not None
                    else pd.NA
                ),
            }
        )

    return pd.DataFrame(rows)
