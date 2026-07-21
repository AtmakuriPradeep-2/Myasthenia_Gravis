from pathlib import Path

import joblib

from app.models.prediction import Prediction

from app.services.alert_service import AlertService
from app.services.feature_service import build_patient_features
from app.services.explanation_service import explain_prediction


# ---------------------------------------------------
# Load Trained Model
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "gradient_boosting_calibrated.joblib"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------
# Development Threshold
# ---------------------------------------------------

DEVELOPMENT_THRESHOLD = 0.20


# ---------------------------------------------------
# Predict Patient Risk
# ---------------------------------------------------

def predict_patient_risk(
    db,
    patient,
    assessments
):

    # ----------------------------------------
    # Build longitudinal features
    # ----------------------------------------

    features = build_patient_features(
        patient,
        assessments
    )

    # ----------------------------------------
    # Predict probability
    # ----------------------------------------

    probability = float(
        model.predict_proba(features)[0][1]
    )

    predicted_risk = (
        probability >= DEVELOPMENT_THRESHOLD
    )

    # ----------------------------------------
    # Risk Category
    # ----------------------------------------

    if probability < 0.10:
        risk_category = "low"

    elif probability < DEVELOPMENT_THRESHOLD:
        risk_category = "moderate"

    else:
        risk_category = "high"

    # ----------------------------------------
    # Generate SHAP Explanation
    # ----------------------------------------

    try:

        explanation = explain_prediction(
            features
        )

    except Exception as e:

        print(
            "SHAP Explanation Error:",
            e
        )

        explanation = []

    # ----------------------------------------
    # Save Prediction
    # ----------------------------------------

    prediction = Prediction(

        patient_id=patient.id,

        probability=probability,

        threshold=DEVELOPMENT_THRESHOLD,

        predicted_event=int(
            predicted_risk
        ),

        risk_category=risk_category,

        model_name="gradient_boosting",

        model_version="development_v0.1"

    )

    db.add(prediction)

    db.commit()

    db.refresh(prediction)

    # ----------------------------------------
    # Create Alert
    # ----------------------------------------

    AlertService.create_alert(

        db=db,

        patient_id=patient.id,

        prediction_id=prediction.id,

        probability=probability

    )

    # ----------------------------------------
    # API Response
    # ----------------------------------------

    return {

        "prediction_id": prediction.id,

        "risk_probability": round(
            probability,
            4
        ),

        "threshold": DEVELOPMENT_THRESHOLD,

        "predicted_worsening_risk": bool(
            predicted_risk
        ),

        "risk_category": risk_category,

        "assessment_count": len(
            assessments
        ),

        "model_name": "gradient_boosting",

        "model_version": "development_v0.1",

        "model_status": "synthetic-data development model",

        # ----------------------------------
        # Explainable AI
        # ----------------------------------

        "top_features": explanation

    }