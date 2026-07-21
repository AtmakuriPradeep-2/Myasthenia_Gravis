from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_code = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    age = Column(
        Integer,
        nullable=False
    )

    sex = Column(
        String,
        nullable=False
    )

    mgfa_class = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )