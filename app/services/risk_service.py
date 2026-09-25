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


class DiabetesRiskService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Diabetes risk model not found: {MODEL_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)

    def predict(self, features: dict) -> dict:
        data = pd.DataFrame([features])

        risk_score = float(
            self.model.predict_proba(data)[0][1]
        )

        if risk_score >= THRESHOLD:
            risk_level = "elevated"
        else:
            risk_level = "low"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
        }


risk_service = DiabetesRiskService()


def predict(self, features: dict) -> dict:
    data = pd.DataFrame([features])

    risk_score = float(
        self.model.predict_proba(data)[0][1]
    )

    if risk_score >= THRESHOLD:
        risk_level = "elevated"
    else:
        risk_level = "low"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
    }