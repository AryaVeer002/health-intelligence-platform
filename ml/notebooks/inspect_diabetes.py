import pandas as pd

DATA_PATH = "ml/data/LLCP2014.XPT"

print("Loading BRFSS dataset...")

df = pd.read_sas(DATA_PATH, format="xport")

print("\nDataset loaded.")
print("Rows:", len(df))

candidate_columns = [
    "DIABETE3",
    "PREDIAB1",
    "_BMI5",
    "_BMI5CAT",
    "_AGEG5YR",
    "GENHLTH",
    "PHYSHLTH",
    "EXERANY2",
    "_TOTINDA",
    "SMOKE100",
    "SMOKDAY2",
    "ALCDAY5",
    "SEX",
    "EDUCA",
    "INCOME2",
]

print("\nChecking candidate variables...\n")

for column in candidate_columns:
    print("=" * 50)
    print(column)

    if column not in df.columns:
        print("NOT FOUND")
        continue

    print("Missing:", df[column].isna().sum())
    print("Unique values:")
    print(df[column].value_counts(dropna=False).head(20))