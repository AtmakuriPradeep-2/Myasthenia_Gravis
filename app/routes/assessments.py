from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.patient import Patient
from app.models.assessment import Assessment
from app.models.user import User

from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse
)

from app.auth.roles import require_clinician


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"]
)


# ------------------------------------
# Get All Clinical Assessments (Clinician & Admin)
# ------------------------------------
@router.get(
    "",
    response_model=list[AssessmentResponse]
)
def get_all_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):
    return (
        db.query(Assessment)
        .order_by(Assessment.observation_date.desc())
        .all()
    )


# ------------------------------------
# Get Assessment By ID (Clinician & Admin)
# ------------------------------------
@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse
)
def get_assessment_by_id(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):


    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment record not found"
        )

    return assessment


# ------------------------------------
# Create Clinical Assessment
# ------------------------------------
@router.post(
    "",
    response_model=AssessmentResponse
)
def create_assessment(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == assessment.patient_id)
        .first()
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_assessment = Assessment(
        patient_id=assessment.patient_id,
        qmg_score=assessment.qmg_score,
        mgc_score=assessment.mgc_score,
        cfq_total=assessment.cfq_total,
        treatment_change=assessment.treatment_change,
        infection_event=assessment.infection_event
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment


# ------------------------------------
# Get Patient Assessments
# ------------------------------------
@router.get(
    "/patient/{patient_id}",
    response_model=list[AssessmentResponse]
)
def get_patient_assessments(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

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

    return assessments