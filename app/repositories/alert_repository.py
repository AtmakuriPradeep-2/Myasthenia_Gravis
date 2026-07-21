from app.models.alert import Alert


class AlertRepository:

    @staticmethod
    def create(
        db,
        alert
    ):

        db.add(alert)

        db.commit()

        db.refresh(alert)

        return alert

    @staticmethod
    def get_all(
        db
    ):

        return db.query(Alert).all()

    @staticmethod
    def get_open_alerts(
        db
    ):

        return (
            db.query(Alert)
            .filter(
                Alert.status == "Open"
            )
            .all()
        )