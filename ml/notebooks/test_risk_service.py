from app.services.risk_service import risk_service


sample_features = {
    "_BMI5": 28.0,
    "_AGEG5YR": 6,
    "SEX": 1,
    "_RFHLTH": 1,
    "PHYSHLTH": 2,
    "_TOTINDA": 1,
    "_RFSMOK3": 1,
    "DRNKANY5": 1,
}


result = risk_service.predict(sample_features)


print()
print("=" * 40)
print("DIABETES RISK SERVICE TEST")
print("=" * 40)

print(f"Risk score : {result['risk_score']:.4f}")
print(f"Risk level : {result['risk_level']}")

print()
print("Explanations:")

for explanation in result["explanations"]:
    print(
        f"  {explanation['factor']}: "
        f"{explanation['contribution']:+.4f} "
        f"({explanation['direction']})"
    )

print("=" * 40)