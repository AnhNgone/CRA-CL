from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
MODELS = ROOT / "models"
REPORTS_FIGURES = ROOT / "reports" / "figures"
DASHBOARDS = ROOT / "dashboards"
DOCS = ROOT / "docs"

ACCEPTED_RAW = DATA_RAW / "accepted_2007_to_2018Q4.csv"
REJECTED_RAW = DATA_RAW / "rejected_2007_to_2018Q4.csv"
DATA_DICTIONARY = DOCS / "LCDataDictionary.xlsx"
