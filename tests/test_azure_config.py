import pytest

from airtraffic.azure import connection_string


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
