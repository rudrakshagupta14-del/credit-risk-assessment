
from pathlib import Path
# Root project folder
BASE_DIR = Path(__file__).resolve().parents[2]
# Saved ML files
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "credit_risk_model.pkl"
COLUMNS_PATH = ARTIFACTS_DIR / "credit_risk_columns.pkl"
