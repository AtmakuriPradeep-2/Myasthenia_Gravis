import pandas as pd


MODEL_FEATURES = [
    "age",
    "sex",
    "mgfa_class",

    "qmg_score",
    "mgc_score",
    "cfq_total_demo",

    "treatment_change",
    "infection_event",

    "qmg_score_previous",
    "qmg_score_change",
    "qmg_score_baseline",
    "qmg_score_baseline_deviation",
    "qmg_score_rolling3_mean",
    "qmg_score_rolling3_std",

    "mgc_score_previous",
    "mgc_score_change",
    "mgc_score_baseline",
    "mgc_score_baseline_deviation",
    "mgc_score_rolling3_mean",
    "mgc_score_rolling3_std",

    "cfq_total_demo_previous",
    "cfq_total_demo_change",
    "cfq_total_demo_baseline",
    "cfq_total_demo_baseline_deviation",
    "cfq_total_demo_rolling3_mean",
    "cfq_total_demo_rolling3_std",

    "days_since_previous",
    "observation_number"
]


def build_patient_features(patient, assessments):

    if not assessments:
        raise ValueError(
            "Patient has no assessments"
        )

    rows = []

    for assessment in assessments:

        rows.append({
            "observation_date":
                assessment.observation_date,

            "qmg_score":
                assessment.qmg_score,

            "mgc_score":
                assessment.mgc_score,

            "cfq_total_demo":
                assessment.cfq_total,

            "treatment_change":
                assessment.treatment_change,

            "infection_event":
                assessment.infection_event
        })

    df = pd.DataFrame(rows)

    df["observation_date"] = pd.to_datetime(
        df["observation_date"]
    )

    df = df.sort_values(
        "observation_date"
    ).reset_index(drop=True)

    # Static patient information
    df["age"] = patient.age
    df["sex"] = patient.sex
    df["mgfa_class"] = patient.mgfa_class

    temporal_columns = [
        "qmg_score",
        "mgc_score",
        "cfq_total_demo"
    ]

    for column in temporal_columns:

        # Previous observation
        df[f"{column}_previous"] = (
            df[column].shift(1)
        )

        # Change from previous observation
        df[f"{column}_change"] = (
            df[column]
            - df[f"{column}_previous"]
        )

        # First recorded assessment as baseline
        df[f"{column}_baseline"] = (
            df[column].iloc[0]
        )

        # Current deviation from baseline
        df[f"{column}_baseline_deviation"] = (
            df[column]
            - df[f"{column}_baseline"]
        )

        # Rolling mean using previous observations only
        df[f"{column}_rolling3_mean"] = (
            df[column]
            .shift(1)
            .rolling(
                window=3,
                min_periods=1
            )
            .mean()
        )

        # Rolling SD using previous observations only
        df[f"{column}_rolling3_std"] = (
            df[column]
            .shift(1)
            .rolling(
                window=3,
                min_periods=2
            )
            .std()
        )

    df["days_since_previous"] = (
        df["observation_date"]
        .diff()
        .dt.days
    )

    df["observation_number"] = (
        range(1, len(df) + 1)
    )

    # Latest assessment row only
    latest_features = df.iloc[[-1]][
        MODEL_FEATURES
    ]

    return latest_features