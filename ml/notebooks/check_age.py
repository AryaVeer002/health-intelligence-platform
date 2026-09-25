import pandas as pd

DATA_PATH = "ml/data/LLCP2014.XPT"

print("Loading BRFSS dataset...")

df = pd.read_sas(DATA_PATH, format="xport")

print("\nChecking AGE variable...")

if "AGE" in df.columns:
    print("AGE FOUND")

    print("\nMissing values:")
    print(df["AGE"].isna().sum())

    print("\nData type:")
    print(df["AGE"].dtype)

    print("\nValue counts:")
    print(df["AGE"].value_counts(dropna=False).sort_index().head(100))

else:
    print("AGE NOT FOUND")

print("\nChecking age-related columns:")

age_columns = [
    column
    for column in df.columns
    if "AGE" in column.upper()
]

print(age_columns)