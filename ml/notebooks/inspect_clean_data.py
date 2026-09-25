import pandas as pd

DATA_PATH = "ml/data/diabetes_clean.csv"

print("Loading cleaned dataset...")

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nUnique values:")
for column in df.columns:
    print(f"\n{column}")
    print(df[column].value_counts().sort_index().head(20))

print("\nTarget distribution:")
print(df["diabetes"].value_counts())

print("\nTarget percentage:")
print(df["diabetes"].value_counts(normalize=True) * 100)

print("\nBasic statistics:")
print(df.describe())