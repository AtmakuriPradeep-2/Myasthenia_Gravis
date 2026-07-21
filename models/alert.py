from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Alert(Base):

    __tablename__="alerts"

    id=Column(Integer,primary_key=True,index=True)

    patient_id=Column(
        Integer,
        ForeignKey("patients.id")
    )

    prediction_id=Column(
        Integer,
        ForeignKey("predictions.id")
    )

    severity=Column(String)

    probability=Column(Float)

    status=Column(
        String,
        default="Open"
    )

    created_at=Column(
        DateTime,
        server_default=func.now()
    )