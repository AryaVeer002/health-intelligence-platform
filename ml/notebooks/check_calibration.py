import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score,
    brier_score_loss,
)
from sklearn.calibration import calibration_curve


DATA_PATH = "ml/data/diabetes_clean.csv"


print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["diabetes"])
y = df["diabetes"]

# Remove socioeconomic features
X = X.drop(columns=["_EDUCAG", "_INCOMG"])


# --------------------------------------------------
# Train / Test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)


# --------------------------------------------------
# Features
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
# Preprocessing
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
# Model
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42,
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# --------------------------------------------------
# Train
# --------------------------------------------------

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Training completed.")


# --------------------------------------------------
# Probabilities
# --------------------------------------------------

probabilities = pipeline.predict_proba(X_test)[:, 1]


# --------------------------------------------------
# Metrics
# --------------------------------------------------

roc_auc = roc_auc_score(
    y_test,
    probabilities,
)

brier = brier_score_loss(
    y_test,
    probabilities,
)


print("\n========================================")
print("CALIBRATION CHECK")
print("========================================")

print("\nROC-AUC:")
print(roc_auc)

print("\nBrier Score:")
print(brier)


# --------------------------------------------------
# Calibration curve
# --------------------------------------------------

fraction_positive, mean_predicted = calibration_curve(
    y_test,
    probabilities,
    n_bins=10,
    strategy="quantile",
)


print("\nCalibration bins:")
print(
    f"{'Mean predicted':<20}"
    f"{'Observed positive':<20}"
)

for predicted, observed in zip(
    mean_predicted,
    fraction_positive,
):
    print(
        f"{predicted:<20.4f}"
        f"{observed:<20.4f}"
    )