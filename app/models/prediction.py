from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    probability = Column(Float, nullable=False)

    threshold = Column(Float, nullable=False)

    predicted_event = Column(Integer)

    risk_category = Column(String)

    model_name = Column(String)

    model_version = Column(String)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )