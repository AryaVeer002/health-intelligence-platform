import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


DATA_PATH = "ml/data/diabetes_clean.csv"


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["diabetes"])
y = df["diabetes"]


# --------------------------------------------------
# 2. Train / Test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
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
    "_EDUCAG",
    "_INCOMG",
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
            OneHotEncoder(handle_unknown="ignore"),
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
# 7. Get feature names
# --------------------------------------------------

feature_names = pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()


# --------------------------------------------------
# 8. Get coefficients
# --------------------------------------------------

coefficients = pipeline.named_steps[
    "model"
].coef_[0]


# --------------------------------------------------
# 9. Create feature importance table
# --------------------------------------------------

importance = pd.DataFrame({
    "feature": feature_names,
    "coefficient": coefficients,
})

importance["absolute_coefficient"] = (
    importance["coefficient"].abs()
)


# --------------------------------------------------
# 10. Sort by absolute importance
# --------------------------------------------------

importance = importance.sort_values(
    "absolute_coefficient",
    ascending=False
)


# --------------------------------------------------
# 11. Display strongest factors
# --------------------------------------------------

print("\n========================================")
print("TOP 20 MODEL FEATURES")
print("========================================")

print(
    importance[
        [
            "feature",
            "coefficient",
            "absolute_coefficient"
        ]
    ].head(20).to_string(index=False)
)


# --------------------------------------------------
# 12. Positive associations
# --------------------------------------------------

print("\n========================================")
print("TOP POSITIVE COEFFICIENTS")
print("========================================")

positive = importance.sort_values(
    "coefficient",
    ascending=False
)

print(
    positive[
        [
            "feature",
            "coefficient"
        ]
    ].head(15).to_string(index=False)
)


# --------------------------------------------------
# 13. Negative associations
# --------------------------------------------------

print("\n========================================")
print("TOP NEGATIVE COEFFICIENTS")
print("========================================")

negative = importance.sort_values(
    "coefficient",
    ascending=True
)

print(
    negative[
        [
            "feature",
            "coefficient"
        ]
    ].head(15).to_string(index=False)
)