from app.models.prediction import Prediction


class PredictionRepository:

    @staticmethod
    def create(
        db,
        prediction
    ):

        db.add(prediction)

        db.commit()

        db.refresh(prediction)

        return prediction

    @staticmethod
    def get_all(
        db
    ):

        return db.query(Prediction).all()

    @staticmethod
    def get_by_patient(
        db,
        patient_id
    ):

        return (
            db.query(Prediction)
            .filter(
                Prediction.patient_id == patient_id
            )
            .all()
        )