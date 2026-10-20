from __future__ import annotations

import re
import unicodedata

import numpy as np
import pandas as pd


AVI0105_YEARS = [str(year) for year in range(2013, 2024)]


def normalize_text(value):
    """Trim whitespace and normalise Unicode without changing meaning."""
    if pd.isna(value):
        return value

    text = unicodedata.normalize("NFKC", str(value))
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_avi0105(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform AVI0105 from wide country/year format to long format.

    Source values are expressed in thousands of passengers.
    """
    cleaned = df.copy()

    cleaned = cleaned.rename(
        columns={
            "Region [Note 3]": "region",
            "Country": "country",
            "% of total in 2023": "pct_of_total_2023",
        }
    )

    cleaned["region"] = cleaned["region"].map(normalize_text)
    cleaned["country"] = cleaned["country"].map(normalize_text)

    cleaned["pct_of_total_2023"] = (
        cleaned["pct_of_total_2023"]
        .astype(str)
        .str.rstrip("%")
        .pipe(pd.to_numeric, errors="coerce")
    )

    long = cleaned.melt(
        id_vars=["region", "country", "pct_of_total_2023"],
        value_vars=AVI0105_YEARS,
        var_name="year",
        value_name="passengers_thousands",
    )

    long["year"] = pd.to_numeric(long["year"], errors="raise").astype(int)
    long["passengers_thousands"] = pd.to_numeric(
        long["passengers_thousands"], errors="raise"
    )

    long["passengers"] = (
        long["passengers_thousands"] * 1000
    ).round().astype("Int64")

    long["source"] = "avi0105"

    return long[
        [
            "region",
            "country",
            "year",
            "passengers",
            "passengers_thousands",
            "pct_of_total_2023",
            "source",
        ]
    ].sort_values(["country", "year"]).reset_index(drop=True)


def clean_avi0301(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise the international-airport benchmark dataset."""
    cleaned = df.rename(
        columns={
            "Rank": "rank",
            "City": "city",
            "Airport": "airport_name",
            "2022 Passenger Numbers (Thousands)": "passengers_2022_thousands",
            "2021 Passenger Numbers (Thousands)": "passengers_2021_thousands",
            "2021-2022 Passenger Number Percentage Change": "passenger_growth_pct",
            "2022 Aircraft Movements (Thousands)": "aircraft_movements_2022_thousands",
            "2021 Aircraft Movements (Thousands)": "aircraft_movements_2021_thousands",
            "2021-2022 Aircraft Movements Percentage Change": "aircraft_movement_growth_pct",
        }
    ).copy()

    cleaned["city"] = cleaned["city"].map(normalize_text)
    cleaned["airport_name"] = cleaned["airport_name"].map(normalize_text)

    cleaned["passengers_2022"] = (
        pd.to_numeric(cleaned["passengers_2022_thousands"], errors="raise") * 1000
    ).astype("Int64")

    cleaned["passengers_2021"] = (
        pd.to_numeric(cleaned["passengers_2021_thousands"], errors="raise") * 1000
    ).astype("Int64")

    cleaned["aircraft_movements_2022"] = (
        pd.to_numeric(
            cleaned["aircraft_movements_2022_thousands"], errors="raise"
        ) * 1000
    ).astype("Int64")

    cleaned["aircraft_movements_2021"] = (
        pd.to_numeric(
            cleaned["aircraft_movements_2021_thousands"], errors="raise"
        ) * 1000
    ).astype("Int64")

    cleaned["source"] = "avi0301"

    return cleaned.reset_index(drop=True)


def clean_sfo(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the SFO passenger-statistics dataset."""
    cleaned = df.copy()

    unnamed = [column for column in cleaned.columns if column.startswith("Unnamed:")]
    cleaned = cleaned.drop(columns=unnamed)

    cleaned = cleaned.rename(
        columns={
            "Activity Period": "activity_period",
            "Activity Period Start Date": "period_start_date",
            "Operating Airline": "operating_airline",
            "Operating Airline IATA Code": "operating_airline_iata",
            "Published Airline": "published_airline",
            "Published Airline IATA Code": "published_airline_iata",
            "GEO Summary": "geo_summary",
            "GEO Region": "geo_region",
            "Activity Type Code": "activity_type",
            "Price Category Code": "price_category",
            "Terminal": "terminal",
            "Boarding Area": "boarding_area",
            "Passenger Count": "passenger_count",
        }
    )

    text_columns = [
        "operating_airline",
        "operating_airline_iata",
        "published_airline",
        "published_airline_iata",
        "geo_summary",
        "geo_region",
        "activity_type",
        "price_category",
        "terminal",
        "boarding_area",
    ]

    for column in text_columns:
        cleaned[column] = cleaned[column].map(normalize_text)

    cleaned["period_start_date"] = pd.to_datetime(
        cleaned["period_start_date"],
        format="%d/%m/%Y",
        errors="raise",
    )

    cleaned["year"] = cleaned["period_start_date"].dt.year
    cleaned["month"] = cleaned["period_start_date"].dt.month

    cleaned["passenger_count"] = pd.to_numeric(
        cleaned["passenger_count"], errors="raise"
    ).astype("Int64")

    cleaned["source"] = "sfo"

    return cleaned.reset_index(drop=True)


def clean_routes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the CAA route-analysis snapshot.

    This dataset represents a current period and its corresponding prior
    period. It must not be interpreted as annual airport history.
    """
    cleaned = df.rename(
        columns={
            "this_period": "period",
            "foreign_region": "destination_region",
            "foreign_country": "destination_country",
            "UK_airport": "uk_airport",
            "foreign_airport": "destination_airport",
            "total_pax_this_period": "passengers_current",
            "total_pax_scheduled_this_period": "scheduled_current",
            "total_pax_charter_this_period": "charter_current",
            "total_pax_last_period": "passengers_prior",
            "total_pax_scheduled_last_period": "scheduled_prior",
            "total_pax_charter_last_period": "charter_prior",
            "total_pax_percent": "source_yoy_pct",
        }
    ).copy()

    for column in [
        "destination_region",
        "destination_country",
        "uk_airport",
        "destination_airport",
    ]:
        cleaned[column] = cleaned[column].map(normalize_text)

    period_text = (
        pd.to_numeric(cleaned["period"], errors="raise")
        .astype(int)
        .astype(str)
        .str.zfill(6)
    )

    cleaned["period_date"] = pd.to_datetime(
        period_text,
        format="%Y%m",
        errors="raise",
    )

    cleaned["current_year"] = cleaned["period_date"].dt.year
    cleaned["current_month"] = cleaned["period_date"].dt.month

    passenger_columns = [
        "passengers_current",
        "scheduled_current",
        "charter_current",
        "passengers_prior",
        "scheduled_prior",
        "charter_prior",
    ]

    for column in passenger_columns:
        cleaned[column] = pd.to_numeric(
            cleaned[column], errors="raise"
        ).astype("Int64")

    current = cleaned["passengers_current"].astype(float)
    prior = cleaned["passengers_prior"].astype(float)

    cleaned["calculated_yoy_pct"] = np.where(
        prior > 0,
        ((current - prior) / prior) * 100,
        np.nan,
    )

    cleaned["source"] = "routes"

    return cleaned.reset_index(drop=True)


def clean_sources(
    datasets: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    """Clean all four canonical source datasets."""
    return {
        "avi0105": clean_avi0105(datasets["avi0105"]),
        "avi0301": clean_avi0301(datasets["avi0301"]),
        "sfo": clean_sfo(datasets["sfo"]),
        "routes": clean_routes(datasets["routes"]),
    }
