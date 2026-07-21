from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database import Base


class Intervention(Base):

    __tablename__ = "interventions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    alert_id = Column(
        Integer,
        ForeignKey("alerts.id"),
        nullable=False
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    clinician = Column(
        String,
        nullable=False
    )

    intervention_type = Column(
        String,
        nullable=False
    )

    notes = Column(
        Text
    )

    follow_up_date = Column(
        Date
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )