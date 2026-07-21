from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.patient import Patient
from app.models.user import User

from app.schemas.patient import (
    PatientCreate,
    PatientResponse
)

from app.auth.roles import require_clinician, require_admin


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


# ------------------------------------
# Get All Patients (Clinician & Admin)
# ------------------------------------
@router.get(
    "",
    response_model=list[PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db),
    _: User = Depends(require_clinician)
):
    return db.query(Patient).order_by(Patient.id.desc()).all()


# ------------------------------------
# Get Patient By ID (Clinician & Admin)
# ------------------------------------
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_clinician)
):


    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )
    return patient


# ------------------------------------
# Create Patient
# ------------------------------------
@router.post(
    "",
    response_model=PatientResponse
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_clinician)
):
    existing = (
        db.query(Patient)
        .filter(Patient.patient_code == patient.patient_code)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient code already exists"
        )

    new_patient = Patient(
        patient_code=patient.patient_code,
        age=patient.age,
        sex=patient.sex,
        mgfa_class=patient.mgfa_class
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# ------------------------------------
# Update Patient
# ------------------------------------
@router.put(
    "/{patient_id}",
    response_model=PatientResponse
)
def update_patient(
    patient_id: int,
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_clinician)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check for patient_code conflict if changed
    if patient.patient_code != patient_data.patient_code:
        conflict = (
            db.query(Patient)
            .filter(Patient.patient_code == patient_data.patient_code)
            .first()
        )
        if conflict:
            raise HTTPException(
                status_code=400,
                detail="Patient code already exists"
            )

    patient.patient_code = patient_data.patient_code
    patient.age = patient_data.age
    patient.sex = patient_data.sex
    patient.mgfa_class = patient_data.mgfa_class

    db.commit()
    db.refresh(patient)

    return patient


# ------------------------------------
# Delete Patient
# ------------------------------------
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_clinician)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }