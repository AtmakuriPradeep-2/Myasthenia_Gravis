from pydantic import BaseModel


class FeatureContribution(BaseModel):

    feature: str

    value: float

    shap_value: float

    impact: str


class PredictionExplanation(BaseModel):

    risk_probability: float

    risk_category: str

    top_features: list[FeatureContribution]