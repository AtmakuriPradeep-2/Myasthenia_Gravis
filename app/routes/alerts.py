from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.alert import Alert
from app.models.user import User

from app.schemas.alert import AlertUpdate

from app.auth.roles import require_clinician


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


# ----------------------------------
# Get All Alerts
# ----------------------------------
@router.get("")
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    return (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )


# ----------------------------------
# Get Open Alerts
# ----------------------------------
@router.get("/open")
def get_open_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    return (
        db.query(Alert)
        .filter(Alert.status == "Open")
        .order_by(Alert.created_at.desc())
        .all()
    )


# ----------------------------------
# Get Alert By ID
# ----------------------------------
@router.get("/{alert_id}")
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


# ----------------------------------
# Review / Update Alert
# ----------------------------------
@router.patch("/{alert_id}")
def update_alert(
    alert_id: int,
    update: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_clinician)
):

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.status = update.status

    alert.reviewed_by = update.reviewed_by

    alert.review_notes = update.review_notes

    alert.reviewed_at = datetime.utcnow()

    if update.status == "Closed":
        alert.closed_at = datetime.utcnow()

    db.commit()
    db.refresh(alert)

    return alert    