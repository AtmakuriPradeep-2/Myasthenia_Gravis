from pydantic import BaseModel
from datetime import datetime


class PredictionResponse(BaseModel):

    id: int

    patient_id: int

    probability: float

    threshold: float

    predicted_event: int

    risk_category: str

    model_name: str

    model_version: str

    created_at: datetime

    class Config:
        from_attributes = True