from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class InterventionCreate(BaseModel):

    alert_id: int

    patient_id: int

    clinician: str

    intervention_type: str

    notes: Optional[str] = None

    follow_up_date: date


class InterventionResponse(BaseModel):

    id: int

    alert_id: int

    patient_id: int

    clinician: str

    intervention_type: str

    notes: Optional[str]

    follow_up_date: date

    created_at: datetime

    class Config:
        from_attributes = True