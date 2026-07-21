from app.models.alert import Alert

class AlertService:

    @staticmethod
    def create_alert(
        db,
        patient_id,
        prediction_id,
        probability
    ):
        # Classify alert severity across 4 levels: Critical (>= 0.80), High (>= 0.50), Moderate (>= 0.20), Low (< 0.20)
        if probability >= 0.80:
            severity = "Critical"
        elif probability >= 0.50:
            severity = "High"
        elif probability >= 0.20:
            severity = "Moderate"
        else:
            severity = "Low"

        alert = Alert(
            patient_id=patient_id,
            prediction_id=prediction_id,
            probability=probability,
            severity=severity,
            status="Open"
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        return alert