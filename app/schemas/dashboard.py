from pydantic import BaseModel


class DashboardSummary(BaseModel):

    total_patients: int

    total_assessments: int

    total_predictions: int

    total_alerts: int

    open_alerts: int

    reviewed_alerts: int

    closed_alerts: int

    total_interventions: int