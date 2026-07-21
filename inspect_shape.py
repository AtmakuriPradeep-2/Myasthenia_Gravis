from pathlib import Path
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "gradient_boosting_calibrated.joblib"

model = joblib.load(MODEL_PATH)

print(type(model))

print("\n========================\n")

print("Number of calibrated classifiers:")
print(len(model.calibrated_classifiers_))

print("\n========================\n")

first = model.calibrated_classifiers_[0]

print(type(first))

print("\n========================\n")

print(dir(first))