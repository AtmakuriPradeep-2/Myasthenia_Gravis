from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.intervention import Intervention
from app.models.user import User

from app.schemas.intervention import (
    InterventionCreate
)

from app.auth.roles import require_clinician


router = APIRouter(
    prefix="/interventions",
    tags=["Interventions"]
)


# --------------------------------
# Create Intervention
# --------------------------------
@router.post("")
def create_intervention(
    intervention: InterventionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    new_intervention = Intervention(
        alert_id=intervention.alert_id,
        patient_id=intervention.patient_id,

        # Use the authenticated clinician
        clinician=current_user.username,

        intervention_type=intervention.intervention_type,
        notes=intervention.notes,
        follow_up_date=intervention.follow_up_date
    )

    db.add(new_intervention)
    db.commit()
    db.refresh(new_intervention)

    return new_intervention


# --------------------------------
# Get All Interventions
# --------------------------------
@router.get("")
def get_interventions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    return (
        db.query(Intervention)
        .order_by(Intervention.created_at.desc())
        .all()
    )


# --------------------------------
# Get Patient Interventions
# --------------------------------
@router.get("/patient/{patient_id}")
def get_patient_interventions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    return (
        db.query(Intervention)
        .filter(
            Intervention.patient_id == patient_id
        )
        .order_by(
            Intervention.created_at.desc()
        )
        .all()
    )


# --------------------------------
# Get Intervention By ID
# --------------------------------
@router.get("/{intervention_id}")
def get_intervention(
    intervention_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    intervention = (
        db.query(Intervention)
        .filter(
            Intervention.id == intervention_id
        )
        .first()
    )

    if intervention is None:
        raise HTTPException(
            status_code=404,
            detail="Intervention not found"
        )

    return intervention