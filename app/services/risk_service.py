from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "ml"
    / "models"
    / "diabetes_risk_model.joblib"
)

THRESHOLD = 0.20


FEATURE_LABELS = {
    "_BMI5": "BMI",
    "_AGEG5YR": "Age group",
    "SEX": "Sex",
    "_RFHLTH": "General health",
    "PHYSHLTH": "Physical health",
    "_TOTINDA": "Physical activity",
    "_RFSMOK3": "Smoking",
    "DRNKANY5": "Alcohol",
}


class DiabetesRiskService:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Diabetes risk model not found: {MODEL_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)

    def _get_feature_group(self, feature_name: str):
        if "BMI5" in feature_name:
            return "_BMI5"

        if "PHYSHLTH" in feature_name:
            return "PHYSHLTH"

        if "AGEG5YR" in feature_name:
            return "_AGEG5YR"

        if "SEX" in feature_name:
            return "SEX"

        if "RFHLTH" in feature_name:
            return "_RFHLTH"

        if "TOTINDA" in feature_name:
            return "_TOTINDA"

        if "RFSMOK3" in feature_name:
            return "_RFSMOK3"

        if "DRNKANY5" in feature_name:
            return "DRNKANY5"

        return None

    def _get_contributions(self, data):

        all_contributions = []

        for calibrated_classifier in (
            self.model.calibrated_classifiers_
        ):

            pipeline = calibrated_classifier.estimator

            preprocessor = pipeline.named_steps[
                "preprocessor"
            ]

            logistic_model = pipeline.named_steps[
                "model"
            ]

            transformed = preprocessor.transform(data)

            if hasattr(transformed, "toarray"):
                transformed = transformed.toarray()

            transformed_values = transformed[0]

            feature_names = (
                preprocessor.get_feature_names_out()
            )

            coefficients = logistic_model.coef_[0]

            contribution_map = {}

            for (
                feature_name,
                value,
                coefficient,
            ) in zip(
                feature_names,
                transformed_values,
                coefficients,
            ):

                group = self._get_feature_group(
                    feature_name
                )

                if group is None:
                    continue

                contribution = float(
                    value * coefficient
                )

                contribution_map[group] = (
                    contribution_map.get(group, 0.0)
                    + contribution
                )

            all_contributions.append(
                contribution_map
            )

        averaged = {}

        for feature in FEATURE_LABELS:

            values = [
                contribution_map.get(
                    feature,
                    0.0
                )
                for contribution_map
                in all_contributions
            ]

            averaged[feature] = (
                sum(values) / len(values)
            )

        return averaged

    def predict(self, features: dict) -> dict:

        data = pd.DataFrame([features])

        risk_score = float(
            self.model.predict_proba(
                data
            )[0][1]
        )

        if risk_score >= THRESHOLD:
            risk_level = "elevated"
        else:
            risk_level = "low"

        contributions = self._get_contributions(
            data
        )

        explanations = []

        for feature, contribution in sorted(
            contributions.items(),
            key=lambda item: abs(item[1]),
            reverse=True,
        ):

            if abs(contribution) < 0.01:
                continue

            if contribution > 0:
                direction = "higher"
            else:
                direction = "lower"

            explanations.append(
                {
                    "factor": FEATURE_LABELS[feature],
                    "contribution": round(
                        contribution,
                        4
                    ),
                    "direction": direction,
                }
            )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "explanations": explanations,
        }


risk_service = DiabetesRiskService()