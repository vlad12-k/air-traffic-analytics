import pytest

from airtraffic.ingest import load_sources, source_summary

pytestmark = pytest.mark.requires_sources


def test_all_four_sources_load():
    datasets = load_sources()

    assert set(datasets) == {
        "avi0105",
        "avi0301",
        "sfo",
        "routes",
    }

    assert all(not frame.empty for frame in datasets.values())


def test_expected_source_row_counts():
    datasets = load_sources()

    assert len(datasets["avi0105"]) == 77
    assert not datasets["avi0301"].empty
    assert len(datasets["sfo"]) == 31339
    assert len(datasets["routes"]) == 1752


def test_source_summary_contains_four_datasets():
    datasets = load_sources()
    summary = source_summary(datasets)

    assert len(summary) == 4
    assert set(summary["dataset"]) == set(datasets)
