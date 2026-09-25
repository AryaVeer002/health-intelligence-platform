import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier


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
    "_EDUCAG",
    "_INCOMG",
]


# --------------------------------------------------
# 4. Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
    ],
    remainder="passthrough",
)


# --------------------------------------------------
# 5. Random Forest
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
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

print("\nTraining Random Forest...")

pipeline.fit(X_train, y_train)

print("Training completed.")


# --------------------------------------------------
# 7. Get feature names
# --------------------------------------------------

feature_names = (
    pipeline
    .named_steps["preprocessor"]
    .get_feature_names_out()
)


# --------------------------------------------------
# 8. Get feature importance
# --------------------------------------------------

importances = (
    pipeline
    .named_steps["model"]
    .feature_importances_
)


importance = pd.DataFrame({
    "feature": feature_names,
    "importance": importances,
})


# --------------------------------------------------
# 9. Sort
# --------------------------------------------------

importance = importance.sort_values(
    "importance",
    ascending=False
)


# --------------------------------------------------
# 10. Display
# --------------------------------------------------

print("\n========================================")
print("TOP 20 RANDOM FOREST FEATURES")
print("========================================")

print(
    importance.head(20).to_string(index=False)
)