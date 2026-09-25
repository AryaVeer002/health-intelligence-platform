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
    confusion_matrix,
)


DATA_PATH = "ml/data/diabetes_clean.csv"


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["diabetes"])
y = df["diabetes"]

# Remove socioeconomic features
X = X.drop(columns=["_EDUCAG", "_INCOMG"])


# --------------------------------------------------
# 2. Train / Test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)


# --------------------------------------------------
# 3. Feature groups
# --------------------------------------------------

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


# --------------------------------------------------
# 4. Preprocessing
# --------------------------------------------------

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


# --------------------------------------------------
# 5. Base model
# --------------------------------------------------

base_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
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


# --------------------------------------------------
# 6. Calibrated model
# --------------------------------------------------

calibrated_model = CalibratedClassifierCV(
    estimator=base_model,
    method="sigmoid",
    cv=5,
)


# --------------------------------------------------
# 7. Train
# --------------------------------------------------

print("\nTraining calibrated Logistic Regression...")

calibrated_model.fit(X_train, y_train)

print("Training completed.")


# --------------------------------------------------
# 8. Predictions
# --------------------------------------------------

probabilities = calibrated_model.predict_proba(X_test)[:, 1]

predictions = (
    probabilities >= 0.50
).astype(int)


# --------------------------------------------------
# 9. Metrics
# --------------------------------------------------

roc_auc = roc_auc_score(
    y_test,
    probabilities,
)

brier = brier_score_loss(
    y_test,
    probabilities,
)

precision = precision_score(
    y_test,
    predictions,
)

recall = recall_score(
    y_test,
    predictions,
)

f1 = f1_score(
    y_test,
    predictions,
)


print("\n========================================")
print("CALIBRATED LOGISTIC REGRESSION")
print("========================================")

print("\nROC-AUC:")
print(roc_auc)

print("\nBrier Score:")
print(brier)

print("\nPrecision:")
print(precision)

print("\nRecall:")
print(recall)

print("\nF1 Score:")
print(f1)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))