from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from app.database import Base


class Assessment(Base):

    __tablename__ = "assessments"

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

    qmg_score = Column(
        Float,
        nullable=False
    )

    mgc_score = Column(
        Float,
        nullable=False
    )

    cfq_total = Column(
        Float,
        nullable=False
    )

    treatment_change = Column(
        Integer,
        default=0
    )

    infection_event = Column(
        Integer,
        default=0
    )

    observation_date = Column(
        DateTime,
        server_default=func.now()
    )