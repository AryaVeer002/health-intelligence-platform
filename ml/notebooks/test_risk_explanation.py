import joblib
import pandas as pd


MODEL_PATH = "ml/models/diabetes_risk_model.joblib"


sample_features = {
    "_BMI5": 28.0,
    "_AGEG5YR": 6,
    "SEX": 1,
    "_RFHLTH": 1,
    "PHYSHLTH": 2,
    "_TOTINDA": 1,
    "_RFSMOK3": 1,
    "DRNKANY5": 1,
}


model = joblib.load(MODEL_PATH)


# Human-readable names for the model feature groups
feature_labels = {
    "_BMI5": "BMI",
    "_AGEG5YR": "Age group",
    "SEX": "Sex",
    "_RFHLTH": "General health",
    "PHYSHLTH": "Physical health",
    "_TOTINDA": "Physical activity",
    "_RFSMOK3": "Smoking",
    "DRNKANY5": "Alcohol",
}


def get_contributions(features):
    data = pd.DataFrame([features])

    all_contributions = []

    for calibrated_classifier in model.calibrated_classifiers_:
        pipeline = calibrated_classifier.estimator

        preprocessor = pipeline.named_steps["preprocessor"]
        logistic_model = pipeline.named_steps["model"]

        transformed = preprocessor.transform(data)

        if hasattr(transformed, "toarray"):
            transformed = transformed.toarray()

        transformed_values = transformed[0]

        feature_names = preprocessor.get_feature_names_out()
        coefficients = logistic_model.coef_[0]

        contribution_map = {}

        for name, value, coefficient in zip(
            feature_names,
            transformed_values,
            coefficients,
        ):
            contribution = float(value * coefficient)

            if "BMI5" in name:
                group = "_BMI5"

            elif "PHYSHLTH" in name:
                group = "PHYSHLTH"

            elif "AGEG5YR" in name:
                group = "_AGEG5YR"

            elif "SEX" in name:
                group = "SEX"

            elif "RFHLTH" in name:
                group = "_RFHLTH"

            elif "TOTINDA" in name:
                group = "_TOTINDA"

            elif "RFSMOK3" in name:
                group = "_RFSMOK3"

            elif "DRNKANY5" in name:
                group = "DRNKANY5"

            else:
                continue

            contribution_map[group] = (
                contribution_map.get(group, 0.0)
                + contribution
            )

        all_contributions.append(contribution_map)

    # Average contribution across the 5 calibrated estimators
    averaged = {}

    for feature in feature_labels:
        values = [
            contribution_map.get(feature, 0.0)
            for contribution_map in all_contributions
        ]

        averaged[feature] = sum(values) / len(values)

    return averaged


contributions = get_contributions(sample_features)


print()
print("=" * 60)
print("MODEL CONTRIBUTION ANALYSIS")
print("=" * 60)

for feature, contribution in sorted(
    contributions.items(),
    key=lambda item: abs(item[1]),
    reverse=True,
):
    direction = (
        "higher model score"
        if contribution > 0
        else "lower model score"
        if contribution < 0
        else "neutral"
    )

    print(
        f"{feature_labels[feature]:25} "
        f"{contribution:+.4f}  "
        f"({direction})"
    )

print("=" * 60)