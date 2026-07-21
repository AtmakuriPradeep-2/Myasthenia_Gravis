from pathlib import Path

import joblib
import shap

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "gradient_boosting_calibrated.joblib"

model = joblib.load(MODEL_PATH)

print(type(model))

print("\n=====================\n")

print(model)