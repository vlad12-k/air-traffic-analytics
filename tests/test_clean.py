import pandas as pd
import pytest

from airtraffic.clean import clean_avi0301, clean_sources
from airtraffic.ingest import load_sources


@pytest.fixture(scope="module")
def cleaned():
    return clean_sources(load_sources())


def test_expected_clean_row_counts(cleaned):
    assert len(cleaned["avi0105"]) == 77 * 11
    assert not cleaned["avi0301"].empty
    assert len(cleaned["sfo"]) == 31339
    assert len(cleaned["routes"]) == 1752


def test_avi0105_is_long_format(cleaned):
    df = cleaned["avi0105"]

    assert set(df["year"].unique()) == set(range(2013, 2024))
    assert df["passengers"].notna().all()
    assert (df["passengers"] >= 0).all()


def test_avi0301_thousands_are_converted_to_counts():
    source = pd.DataFrame(
        {
            "Rank": [1],
            "City": ["Example City"],
            "Airport": ["Example International Airport"],
            "2022 Passenger Numbers (Thousands)": [12.5],
            "2021 Passenger Numbers (Thousands)": [11.0],
            "2021-2022 Passenger Number Percentage Change": [13.6],
            "2022 Aircraft Movements (Thousands)": [0.5],
            "2021 Aircraft Movements (Thousands)": [0.4],
            "2021-2022 Aircraft Movements Percentage Change": [25.0],
        }
    )

    cleaned = clean_avi0301(source)
    row = cleaned.iloc[0]

    assert row["airport_name"] == "Example International Airport"
    assert row["passengers_2022"] == 12_500
    assert row["passengers_2021"] == 11_000
    assert row["aircraft_movements_2022"] == 500


def test_sfo_removes_empty_unnamed_columns(cleaned):
    df = cleaned["sfo"]

    assert not any(column.startswith("Unnamed:") for column in df.columns)
    assert pd.api.types.is_datetime64_any_dtype(df["period_start_date"])
    assert df["passenger_count"].notna().all()


def test_routes_preserve_current_and_prior_periods(cleaned):
    df = cleaned["routes"]

    assert df["period_date"].notna().all()
    assert df["passengers_current"].notna().all()
    assert df["passengers_prior"].notna().all()

    assert (df["passengers_current"] >= 0).all()
    assert (df["passengers_prior"] >= 0).all()


def test_routes_do_not_fabricate_2019_history(cleaned):
    df = cleaned["routes"]

    assert "recovery_vs_2019_pct" not in df.columns
