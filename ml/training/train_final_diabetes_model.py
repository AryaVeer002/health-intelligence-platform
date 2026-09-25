import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# =========================
# PATHS
# =========================

DATA_PATH = "ml/data/diabetes_clean.csv"
MODEL_PATH = "ml/models/diabetes_risk_model.joblib"
METADATA_PATH = "ml/models/diabetes_risk_model_metadata.json"


# =========================
# LOAD DATA
# =========================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["diabetes"])
y = df["diabetes"]


# =========================
# FINAL FEATURES
# =========================

# Socioeconomic features were excluded
# after the feature experiment.
X = X.drop(columns=["_EDUCAG", "_INCOMG"])

numeric_features = [
    "_BMI5",
    "PHYSHLTH",
]

categorical_features = [
    "_AGEG5YR",
    "SEX",
    "_RFHLTH",
    "_TOTINDA",
    "_RFSMOK3",
    "DRNKANY5",
]


# =========================
# PREPROCESSING
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            StandardScaler(),
            numeric_features,
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                drop="first",
            ),
            categorical_features,
        ),
    ]
)


# =========================
# BASE MODEL
# =========================

base_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "model",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ]
)


# =========================
# CALIBRATED MODEL
# =========================

print("Training calibrated model...")

model = CalibratedClassifierCV(
    estimator=base_model,
    method="sigmoid",
    cv=5,
)

model.fit(X, y)

print("Training completed.")


# =========================
# SAVE MODEL
# =========================

Path("ml/models").mkdir(
    parents=True,
    exist_ok=True,
)

joblib.dump(
    model,
    MODEL_PATH,
)


# =========================
# SAVE METADATA
# =========================

metadata = {
    "model_name": "Diabetes Risk Model",
    "model_version": "1.0",
    "dataset": "CDC BRFSS 2014",
    "algorithm": "Calibrated Logistic Regression",
    "calibration": "Sigmoid",
    "threshold": 0.20,
    "target": "diabetes",
    "excluded_features": [
        "_EDUCAG",
        "_INCOMG",
    ],
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
    "roc_auc": 0.8122673948108469,
    "brier_score": 0.09749404162649433,
    "threshold_precision": 0.3656,
    "threshold_recall": 0.5719,
    "threshold_f1": 0.4460,
    "note": (
        "Model-based risk indicator using observational "
        "BRFSS 2014 data. Not a clinical diagnosis."
    ),
}

with open(
    METADATA_PATH,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        metadata,
        file,
        indent=4,
    )


# =========================
# COMPLETE
# =========================

print()
print("=" * 45)
print("FINAL MODEL SAVED")
print("=" * 45)
print(f"Model:    {MODEL_PATH}")
print(f"Metadata: {METADATA_PATH}")
print(f"Features: {len(numeric_features) + len(categorical_features)}")
print("Threshold: 0.20")