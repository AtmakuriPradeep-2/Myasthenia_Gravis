from pydantic import BaseModel
from datetime import datetime


class AssessmentCreate(BaseModel):
    patient_id: int
    qmg_score: float
    mgc_score: float
    cfq_total: float
    treatment_change: int = 0
    infection_event: int = 0


class AssessmentResponse(AssessmentCreate):
    id: int
    observation_date: datetime

    class Config:
        from_attributes = True