from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.auth.roles import require_roles

from app.services.dashboard_service import (
    get_dashboard_summary,
    get_risk_distribution,
    get_alert_statistics,
    get_intervention_statistics,
    get_patient_statistics,
    get_prediction_trends,
    get_recent_predictions,
    get_ai_insights,
    get_model_performance
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ---------------------------------------
# Dashboard Summary
# ---------------------------------------
@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_dashboard_summary(db)


# ---------------------------------------
# Risk Distribution
# ---------------------------------------
@router.get("/risk-distribution")
def risk_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_risk_distribution(db)


# ---------------------------------------
# Alert Statistics
# ---------------------------------------
@router.get("/alert-statistics")
def alert_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_alert_statistics(db)


# ---------------------------------------
# Intervention Statistics
# ---------------------------------------
@router.get("/intervention-statistics")
def intervention_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_intervention_statistics(db)


# ---------------------------------------
# Patient Statistics
# ---------------------------------------
@router.get("/patient-statistics")
def patient_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_patient_statistics(db)


# ---------------------------------------
# Prediction Trends
# ---------------------------------------
@router.get("/prediction-trends")
def prediction_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_prediction_trends(db)


# ---------------------------------------
# Recent Predictions
# ---------------------------------------
@router.get("/recent-predictions")
def recent_predictions(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_recent_predictions(db)


# ---------------------------------------
# AI Insights
# ---------------------------------------
@router.get("/ai-insights")
def ai_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_ai_insights(db)


# ---------------------------------------
# Model Performance
# ---------------------------------------
@router.get("/model-performance")
def model_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles([
            "Admin",
            "Researcher",
            "Clinician"
        ])
    )
):
    return get_model_performance(db)