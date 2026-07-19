from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

OUTPUT_JSON_DIR = BASE_DIR / "outputs" / "json"
OUTPUT_CSV_DIR = BASE_DIR / "outputs" / "csv"
OUTPUT_CHART_DIR = BASE_DIR / "outputs" / "charts"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_JSON_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CHART_DIR.mkdir(parents=True, exist_ok=True)