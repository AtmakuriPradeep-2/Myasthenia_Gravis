from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.patient import Patient
from app.models.assessment import Assessment
from app.models.prediction import Prediction
from app.models.user import User

from app.services.prediction_service import predict_patient_risk

from app.auth.roles import require_clinician

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)

# -----------------------------------
# Generate Prediction
# -----------------------------------
@router.post("/{patient_id}")
def predict_risk(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    assessments = (
        db.query(Assessment)
        .filter(
            Assessment.patient_id == patient_id
        )
        .order_by(
            Assessment.observation_date.asc()
        )
        .all()
    )

    if len(assessments) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 assessments are required"
        )

    result = predict_patient_risk(
        db,
        patient,
        assessments
    )

    return {
        "patient_id": patient.id,
        "patient_code": patient.patient_code,
        **result
    }


# -----------------------------------
# Get All Predictions (Clinician & Admin)
# -----------------------------------
@router.get("")
def get_predictions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    return (
        db.query(Prediction)
        .order_by(
            Prediction.created_at.desc()
        )
        .all()
    )


# -----------------------------------
# Get Patient Prediction History (Clinician & Admin)
# -----------------------------------
@router.get("/patient/{patient_id}")
def get_patient_predictions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):



    return (
        db.query(Prediction)
        .filter(
            Prediction.patient_id == patient_id
        )
        .order_by(
            Prediction.created_at.desc()
        )
        .all()
    )