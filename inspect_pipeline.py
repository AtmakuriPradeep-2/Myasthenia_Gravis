from pathlib import Path
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "gradient_boosting_calibrated.joblib"

model = joblib.load(MODEL_PATH)

pipeline = model.calibrated_classifiers_[0].estimator

print("Pipeline Steps:")
print(pipeline.named_steps.keys())

print("\n========================")

preprocessor = pipeline.named_steps["preprocessing"]

print(type(preprocessor))

print("\n========================")

print("Transformed Feature Names:")

try:
    feature_names = preprocessor.get_feature_names_out()
    print(feature_names)
except Exception as e:
    print(e)