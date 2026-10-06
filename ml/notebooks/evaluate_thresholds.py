import pandas as pd

from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    brier_score_loss,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ==================================================
# CONFIGURATION
# ==================================================

DATA_PATH = "ml/data/diabetes_clean.csv"

TEST_SIZE = 0.20
VALIDATION_SIZE = 0.20

RANDOM_STATE = 42

THRESHOLDS = [
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
]


# ==================================================
# 1. LOAD DATA
# ==================================================

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["diabetes"])
y = df["diabetes"]


# ==================================================
# 2. REMOVE EXCLUDED FEATURES
# ==================================================

X = X.drop(
    columns=[
        "_EDUCAG",
        "_INCOMG",
    ]
)


# ==================================================
# 3. DEVELOPMENT / TEST SPLIT
# ==================================================

X_development, X_test, y_development, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)


# ==================================================
# 4. TRAIN / VALIDATION SPLIT
# ==================================================

X_train, X_validation, y_train, y_validation = train_test_split(
    X_development,
    y_development,
    test_size=VALIDATION_SIZE,
    random_state=RANDOM_STATE,
    stratify=y_development,
)


print()
print("=" * 60)
print("DATA SPLIT")
print("=" * 60)

print(f"Total records:       {len(df)}")
print(f"Training records:    {len(X_train)}")
print(f"Validation records:  {len(X_validation)}")
print(f"Test records:        {len(X_test)}")


# ==================================================
# 5. FEATURES
# ==================================================

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


# ==================================================
# 6. PREPROCESSING
# ==================================================

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


# ==================================================
# 7. BASE MODEL
# ==================================================

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


# ==================================================
# 8. CALIBRATED MODEL
# ==================================================

print()
print("Training calibrated model...")

model = CalibratedClassifierCV(
    estimator=base_model,
    method="sigmoid",
    cv=5,
    ensemble=True,
)

model.fit(
    X_train,
    y_train,
)

print("Training completed.")


# ==================================================
# 9. VALIDATION PREDICTIONS
# ==================================================

validation_probabilities = model.predict_proba(
    X_validation
)[:, 1]


# ==================================================
# 10. SELECT THRESHOLD USING VALIDATION SET
# ==================================================

print()
print("=" * 60)
print("VALIDATION THRESHOLD ANALYSIS")
print("=" * 60)

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
)

print("-" * 48)


best_threshold = None
best_f1 = -1


for threshold in THRESHOLDS:

    validation_predictions = (
        validation_probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_validation,
        validation_predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_validation,
        validation_predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_validation,
        validation_predictions,
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


# ==================================================
# 11. FINAL TEST EVALUATION
# ==================================================

print()
print("=" * 60)
print("FINAL TEST EVALUATION")
print("=" * 60)

print(
    f"Selected threshold: {best_threshold:.2f}"
)


test_probabilities = model.predict_proba(
    X_test
)[:, 1]


test_predictions = (
    test_probabilities >= best_threshold
).astype(int)


# ==================================================
# 12. TEST METRICS
# ==================================================

roc_auc = roc_auc_score(
    y_test,
    test_probabilities,
)

brier_score = brier_score_loss(
    y_test,
    test_probabilities,
)

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


print(
    f"ROC-AUC:     {roc_auc:.6f}"
)

print(
    f"Brier Score: {brier_score:.6f}"
)

print(
    f"Precision:   {test_precision:.6f}"
)

print(
    f"Recall:      {test_recall:.6f}"
)

print(
    f"F1 Score:    {test_f1:.6f}"
)


# ==================================================
# 13. COMPLETE
# ==================================================

print()
print("=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)