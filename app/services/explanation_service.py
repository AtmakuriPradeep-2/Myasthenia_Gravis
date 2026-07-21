import numpy as np
import pandas as pd

from app.services.shap_service import (
    preprocessor,
    explainer
)

from app.services.feature_name_mapper import (
    FEATURE_NAME_MAP
)


def explain_prediction(features: pd.DataFrame):

    # Transform features exactly as model training
    transformed = preprocessor.transform(features)

    # Get transformed feature names
    feature_names = preprocessor.get_feature_names_out()

    # Calculate SHAP values
    shap_values = explainer.shap_values(transformed)

    # Handle binary classification output
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap_values = shap_values[0]

    transformed = transformed[0]

    results = []

    for feature, value, shap_value in zip(
        feature_names,
        transformed,
        shap_values
    ):

        results.append({

            "feature": FEATURE_NAME_MAP.get(
                feature,
                feature
            ),

            "value": round(float(value), 3),

            "shap_value": round(float(shap_value), 4),

            "impact": (
                "Increase Risk"
                if shap_value > 0
                else "Decrease Risk"
            )

        })

    # Sort by SHAP importance
    results = sorted(
        results,
        key=lambda x: abs(x["shap_value"]),
        reverse=True
    )

    # Return Top 5 features
    return results[:5]