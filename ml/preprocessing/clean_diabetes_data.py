import pandas as pd

DATA_PATH = "ml/data/LLCP2014.XPT"
OUTPUT_PATH = "ml/data/diabetes_clean.csv"

FEATURES = [
    "_BMI5",
    "_AGEG5YR",
    "SEX",
    "_RFHLTH",
    "PHYSHLTH",
    "_TOTINDA",
    "_RFSMOK3",
    "DRNKANY5",
    "_EDUCAG",
    "_INCOMG",
]

TARGET = "DIABETE3"

print("Loading BRFSS dataset...")

df = pd.read_sas(DATA_PATH, format="xport")

print(f"Original rows: {len(df)}")

# --------------------------------------------------
# 1. Keep only required columns
# --------------------------------------------------

columns = FEATURES + [TARGET]

df = df[columns].copy()

print(f"Rows after column selection: {len(df)}")

# --------------------------------------------------
# 2. Keep only valid diabetes target responses
# --------------------------------------------------

df = df[df[TARGET].isin([1.0, 3.0])].copy()

# Convert:
# 1 = diabetes
# 3 = no diabetes

df["diabetes"] = df[TARGET].map({
    1.0: 1,
    3.0: 0
})

df.drop(columns=[TARGET], inplace=True)

print(f"Rows after target cleaning: {len(df)}")

# --------------------------------------------------
# 3. Convert BMI
# --------------------------------------------------

df["_BMI5"] = df["_BMI5"] / 100

# --------------------------------------------------
# 4. Replace invalid calculated-variable codes
# --------------------------------------------------

invalid_codes = {
    "_RFHLTH": [9],
    "_TOTINDA": [9],
    "_RFSMOK3": [9],
    "DRNKANY5": [7, 9],
    "_EDUCAG": [9],
    "_INCOMG": [9],
}

for column, codes in invalid_codes.items():
    df[column] = df[column].replace(codes, pd.NA)

# --------------------------------------------------
# 5. Remove rows missing required features
# --------------------------------------------------

print("\nMissing values before cleaning:")

print(df.isna().sum())

df.dropna(inplace=True)

print(f"\nRows after removing missing values: {len(df)}")

# --------------------------------------------------
# 6. Save cleaned dataset
# --------------------------------------------------

df.to_csv(OUTPUT_PATH, index=False)

print(f"\nClean dataset saved to: {OUTPUT_PATH}")

# --------------------------------------------------
# 7. Final summary
# --------------------------------------------------

print("\nFinal dataset shape:")
print(df.shape)

print("\nTarget distribution:")
print(df["diabetes"].value_counts())

print("\nFirst 5 rows:")
print(df.head())