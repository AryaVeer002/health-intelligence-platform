import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)


DATA_PATH = "ml/data/diabetes_clean.csv"


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["diabetes"])
y = df["diabetes"]


# Remove socioeconomic features
X = X.drop(columns=["_EDUCAG", "_INCOMG"])


# --------------------------------------------------
# 2. Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)


# --------------------------------------------------
# 3. Features
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
# 5. Model
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
# 6. Train
# --------------------------------------------------

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Training completed.")


# --------------------------------------------------
# 7. Probability predictions
# --------------------------------------------------

probabilities = pipeline.predict_proba(X_test)[:, 1]


# --------------------------------------------------
# 8. Threshold evaluation
# --------------------------------------------------

thresholds = [
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


print("\n========================================")
print("THRESHOLD ANALYSIS")
print("========================================")

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
)


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    print(
        f"{threshold:<12.2f}"
        f"{precision:<12.4f}"
        f"{recall:<12.4f}"
        f"{f1:<12.4f}"
    )