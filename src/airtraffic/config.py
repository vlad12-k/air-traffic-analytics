from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
GOLDEN_DIR = OUTPUTS_DIR / "golden"
PLOTS_DIR = OUTPUTS_DIR / "plots"
QA_DIR = OUTPUTS_DIR / "qa"

SOURCE_FILES = {
    "avi0105": RAW_DATA_DIR / "AVI0105.csv",
    "avi0301": RAW_DATA_DIR / "AVI0301.csv",
    "sfo": RAW_DATA_DIR / "Air_Traffic_Passenger_Statistics_2005-2020.csv",
    "routes": RAW_DATA_DIR / "Table_12_1_Intl_Air_Pax_Traffic_Route_Analysis.csv",
}
