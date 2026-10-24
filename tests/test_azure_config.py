from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from airtraffic.azure import (
    connection_string,
    normalise_scalar,
    quote_odbc,
    utc_naive,
)


def test_connection_string_requires_explicit_azure_configuration(monkeypatch):
    for name in (
        "AZURE_SQL_SERVER",
        "AZURE_SQL_DATABASE",
        "AZURE_SQL_USERNAME",
    ):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(ValueError, match="AZURE_SQL_SERVER"):
        connection_string("not-a-real-password")


def test_connection_string_uses_environment_configuration(monkeypatch):
    monkeypatch.setenv("AZURE_SQL_SERVER", "sql.example.invalid")
    monkeypatch.setenv("AZURE_SQL_DATABASE", "analytics_test")
    monkeypatch.setenv("AZURE_SQL_USERNAME", "release_test_user")

    value = connection_string("test-password")

    assert "SERVER=tcp:sql.example.invalid,1433" in value
    assert "DATABASE=analytics_test" in value
    assert "UID={release_test_user}" in value
    assert "PWD={test-password}" in value
    assert "TrustServerCertificate=no" in value


def test_quote_odbc_escapes_closing_braces():
    assert quote_odbc("service}name") == "{service}}name}"


def test_utc_naive_normalizes_offset_to_utc():
    assert utc_naive("2026-02-03T12:30:00+02:00") == datetime(
        2026, 2, 3, 10, 30
    )


def test_utc_naive_treats_naive_timestamp_as_utc():
    assert utc_naive("2026-02-03T10:30:00") == datetime(
        2026, 2, 3, 10, 30
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (np.int64(7), 7),
        (np.float64(1.25), 1.25),
        (pd.NA, None),
        (float("nan"), None),
    ],
)
def test_normalise_scalar_handles_numeric_and_missing_values(value, expected):
    actual = normalise_scalar(value)
    assert actual == expected
    if expected is not None:
        assert type(actual) is type(expected)


def test_normalise_scalar_converts_naive_timestamp_to_datetime():
    value = pd.Timestamp(datetime(2026, 2, 3, 10, 30))
    actual = normalise_scalar(value)
    assert actual == datetime(2026, 2, 3, 10, 30)
    assert actual.tzinfo is None
