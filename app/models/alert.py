from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.sql import func

from app.database import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    prediction_id = Column(
        Integer,
        ForeignKey("predictions.id"),
        nullable=False
    )

    probability = Column(Float)

    severity = Column(String)

    status = Column(
        String,
        default="Open"
    )

    reviewed_by = Column(
        String,
        nullable=True
    )

    review_notes = Column(
        Text,
        nullable=True
    )

    reviewed_at = Column(
        DateTime,
        nullable=True
    )

    closed_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )