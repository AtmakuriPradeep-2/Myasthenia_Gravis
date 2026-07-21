from pathlib import Path

import joblib
import shap

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "models" / "gradient_boosting_calibrated.joblib"

model = joblib.load(MODEL_PATH)

# Extract the trained pipeline from the first calibrated classifier
pipeline = model.calibrated_classifiers_[0].estimator

preprocessor = pipeline.named_steps["preprocessing"]

classifier = pipeline.named_steps["classifier"]

explainer = shap.TreeExplainer(classifier)