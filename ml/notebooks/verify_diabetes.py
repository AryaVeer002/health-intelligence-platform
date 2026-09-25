import pandas as pd

DATA_PATH = "ml/data/LLCP2014.XPT"

print("Loading BRFSS dataset...")
df = pd.read_sas(DATA_PATH, format="xport")

print("\nDIABETE3 value counts:")
print(df["DIABETE3"].value_counts(dropna=False).sort_index())

print("\nDIABETE3 data type:")
print(df["DIABETE3"].dtype)

print("\nPotential target values:")
print(sorted(df["DIABETE3"].dropna().unique()))