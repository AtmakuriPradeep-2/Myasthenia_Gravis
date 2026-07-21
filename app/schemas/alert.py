from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertUpdate(BaseModel):

    status: str

    reviewed_by: Optional[str] = None

    review_notes: Optional[str] = None


class AlertResponse(BaseModel):

    id: int

    patient_id: int

    prediction_id: int

    probability: float

    severity: str

    status: str

    reviewed_by: Optional[str]

    review_notes: Optional[str]

    reviewed_at: Optional[datetime]

    closed_at: Optional[datetime]

    created_at: datetime

    class Config:
        from_attributes = True