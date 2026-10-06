import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    roc_auc_score,
    brier_score_loss,
    precision_score,
    recall_score,
    f1_score,
)


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "ml/data/diabetes_clean.csv"

RANDOM_STATE = 42

# 20% of the complete dataset is kept completely independent
TEST_SIZE = 0.20

# 20% of the remaining 80% is used for validation
# Final proportions:
# Training    = 64%
# Validation  = 16%
# Test        = 20%

VALIDATION_SIZE = 0.20

THRESHOLDS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
]


# ============================================================
# LOAD DATA
# ============================================================

print("========================================")
print("DIABETES MODEL EVALUATION")
print("========================================")

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Total rows: {len(df):,}")

X = df.drop(columns=["diabetes"])
y = df["diabetes"]


# ============================================================
# REMOVE EXCLUDED FEATURES
# ============================================================

X = X.drop(columns=["_EDUCAG", "_INCOMG"])


# ============================================================
# FEATURE GROUPS
# ============================================================

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


# ============================================================
# STEP 1 — INDEPENDENT TEST SET
# ============================================================

print("\nCreating independent test set...")

X_development, X_test, y_development, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)

print(f"Development rows: {len(X_development):,}")
print(f"Independent test rows: {len(X_test):,}")


# ============================================================
# STEP 2 — TRAIN / VALIDATION SPLIT
# ============================================================

print("\nCreating validation set...")

X_train, X_validation, y_train, y_validation = train_test_split(
    X_development,
    y_development,
    test_size=VALIDATION_SIZE,
    random_state=RANDOM_STATE,
    stratify=y_development,
)

print(f"Training rows: {len(X_train):,}")
print(f"Validation rows: {len(X_validation):,}")
print(f"Independent test rows: {len(X_test):,}")


# ============================================================
# PREPROCESSING
# ============================================================

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


# ============================================================
# BASE MODEL
# ============================================================

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
                random_state=RANDOM_STATE,
            ),
        ),
    ]
)


# ============================================================
# CALIBRATED MODEL
# ============================================================

model = CalibratedClassifierCV(
    estimator=base_model,
    method="sigmoid",
    cv=5,
    ensemble=True,
)


# ============================================================
# TRAIN
# ============================================================

print("\n========================================")
print("TRAINING CALIBRATED MODEL")
print("========================================")

model.fit(
    X_train,
    y_train,
)

print("Training completed.")


# ============================================================
# VALIDATION PROBABILITIES
# ============================================================

print("\nGenerating validation probabilities...")

validation_probabilities = model.predict_proba(
    X_validation
)[:, 1]


# ============================================================
# THRESHOLD SELECTION
# ============================================================

print("\n========================================")
print("VALIDATION THRESHOLD ANALYSIS")
print("========================================")

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
)

best_threshold = None
best_f1 = -1.0

for threshold in THRESHOLDS:

    predictions = (
        validation_probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_validation,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_validation,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_validation,
        predictions,
        zero_division=0,
    )

    print(
        f"{threshold:<12.2f}"
        f"{precision:<12.4f}"
        f"{recall:<12.4f}"
        f"{f1:<12.4f}"
    )

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold


print("\nSelected threshold:")
print(f"{best_threshold:.2f}")

print(f"Validation F1: {best_f1:.4f}")


# ============================================================
# INDEPENDENT TEST EVALUATION
# ============================================================

print("\n========================================")
print("INDEPENDENT TEST EVALUATION")
print("========================================")

test_probabilities = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# PROBABILITY METRICS
# ============================================================

roc_auc = roc_auc_score(
    y_test,
    test_probabilities,
)

brier_score = brier_score_loss(
    y_test,
    test_probabilities,
)


# ============================================================
# THRESHOLD METRICS
# ============================================================

test_predictions = (
    test_probabilities >= best_threshold
).astype(int)

test_precision = precision_score(
    y_test,
    test_predictions,
    zero_division=0,
)

test_recall = recall_score(
    y_test,
    test_predictions,
    zero_division=0,
)

test_f1 = f1_score(
    y_test,
    test_predictions,
    zero_division=0,
)


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n========================================")
print("FINAL TEST METRICS")
print("========================================")

print(f"ROC-AUC:          {roc_auc:.6f}")
print(f"Brier Score:      {brier_score:.6f}")
print(f"Threshold:        {best_threshold:.2f}")
print(f"Precision:        {test_precision:.6f}")
print(f"Recall:           {test_recall:.6f}")
print(f"F1 Score:         {test_f1:.6f}")


# ============================================================
# DATASET SUMMARY
# ============================================================

print("\n========================================")
print("DATASET SUMMARY")
print("========================================")

print(f"Total dataset:       {len(df):,}")
print(f"Training set:        {len(X_train):,}")
print(f"Validation set:      {len(X_validation):,}")
print(f"Independent test:    {len(X_test):,}")


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

print("\nTarget distribution:")

print(
    y.value_counts()
    .sort_index()
)


# ============================================================
# COMPLETION
# ============================================================

print("\n========================================")
print("EVALUATION COMPLETE")
print("========================================")

print(
    "Threshold was selected using validation data."
)

print(
    "Final metrics were calculated using the "
    "independent test set."
)

print(
    "The independent test set was not used "
    "for threshold selection."
)