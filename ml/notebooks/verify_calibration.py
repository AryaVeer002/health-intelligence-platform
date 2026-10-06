from pathlib import Path

import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = Path("ml/data/diabetes_clean.csv")

TARGET = "diabetes"

NUMERIC_FEATURES = [
    "_BMI5",
    "PHYSHLTH",
]

CATEGORICAL_FEATURES = [
    "_AGEG5YR",
    "SEX",
    "_RFHLTH",
    "_TOTINDA",
    "_RFSMOK3",
    "DRNKANY5",
]

RANDOM_STATE = 42
TEST_SIZE = 0.20
VALIDATION_SIZE = 0.20


# ============================================================
# LOAD DATA
# ============================================================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y = df[TARGET]


# ============================================================
# THREE-WAY SPLIT
# ============================================================

X_dev, X_test, y_dev, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    stratify=y,
    random_state=RANDOM_STATE,
)

X_train, X_validation, y_train, y_validation = train_test_split(
    X_dev,
    y_dev,
    test_size=VALIDATION_SIZE,
    stratify=y_dev,
    random_state=RANDOM_STATE,
)

print()
print("=" * 60)
print("DATA SPLIT")
print("=" * 60)

print(f"Total records:       {len(df)}")
print(f"Training records:    {len(X_train)}")
print(f"Validation records:  {len(X_validation)}")
print(f"Test records:        {len(X_test)}")


# ============================================================
# PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            NUMERIC_FEATURES,
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                drop="first",
            ),
            CATEGORICAL_FEATURES,
        ),
    ]
)


# ============================================================
# BASE MODEL
# ============================================================

base_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=RANDOM_STATE,
)


# ============================================================
# UNCALIBRATED MODEL
# ============================================================

print()
print("Training uncalibrated model...")

uncalibrated_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", base_model),
    ]
)

uncalibrated_model.fit(X_train, y_train)

uncalibrated_probabilities = (
    uncalibrated_model.predict_proba(X_test)[:, 1]
)


# ============================================================
# CALIBRATED MODEL
# ============================================================

print("Training calibrated model...")

calibrated_classifier = CalibratedClassifierCV(
    estimator=base_model,
    method="sigmoid",
    cv=5,
    ensemble=True,
)

calibrated_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", calibrated_classifier),
    ]
)

calibrated_model.fit(X_train, y_train)

calibrated_probabilities = (
    calibrated_model.predict_proba(X_test)[:, 1]
)


# ============================================================
# EVALUATION
# ============================================================

uncalibrated_brier = brier_score_loss(
    y_test,
    uncalibrated_probabilities,
)

calibrated_brier = brier_score_loss(
    y_test,
    calibrated_probabilities,
)

uncalibrated_auc = roc_auc_score(
    y_test,
    uncalibrated_probabilities,
)

calibrated_auc = roc_auc_score(
    y_test,
    calibrated_probabilities,
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 60)
print("CALIBRATION COMPARISON")
print("=" * 60)

print(
    f"{'Model':<20}"
    f"{'ROC-AUC':>12}"
    f"{'Brier Score':>15}"
)

print("-" * 60)

print(
    f"{'Uncalibrated':<20}"
    f"{uncalibrated_auc:>12.6f}"
    f"{uncalibrated_brier:>15.6f}"
)

print(
    f"{'Sigmoid calibrated':<20}"
    f"{calibrated_auc:>12.6f}"
    f"{calibrated_brier:>15.6f}"
)

print()
print("=" * 60)
print("Brier SCORE CHANGE")
print("=" * 60)

change = calibrated_brier - uncalibrated_brier

print(f"Uncalibrated Brier: {uncalibrated_brier:.6f}")
print(f"Calibrated Brier:   {calibrated_brier:.6f}")
print(f"Change:             {change:+.6f}")

if calibrated_brier < uncalibrated_brier:
    print("Result: calibrated model has lower Brier score.")
elif calibrated_brier > uncalibrated_brier:
    print("Result: calibrated model has higher Brier score.")
else:
    print("Result: Brier scores are equal.")

print()
print("=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)