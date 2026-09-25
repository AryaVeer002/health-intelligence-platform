import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PATH = "ml/data/diabetes_clean.csv"

print("Loading cleaned dataset...")

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["diabetes"])
y = df["diabetes"]

print("\nOriginal dataset:")
print("X shape:", X.shape)
print("y shape:", y.shape)

# Stratified 80/20 split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTrain set:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("\nTest set:")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)

print("\nTraining target distribution:")
print(y_train.value_counts(normalize=True) * 100)

print("\nTest target distribution:")
print(y_test.value_counts(normalize=True) * 100)

print("\nSplit completed successfully.")