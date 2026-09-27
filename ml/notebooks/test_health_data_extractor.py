from app.services.health_data_extractor import (
    health_data_extractor
)


sample_text = """
Patient Health Report
Report Date: 2025-01-15
BMI: 28.5
Heart Rate: 82
Blood Pressure: 130/85
Physical Activity: Regular
"""


result = health_data_extractor.extract(
    sample_text
)


print()

print("=" * 40)
print("HEALTH DATA EXTRACTION TEST")
print("=" * 40)

print(
    "Report Date: "
    f"{result.get('report_date')}"
)

print(f"BMI: {result.get('bmi')}")

print(
    f"Heart Rate: "
    f"{result.get('heart_rate')}"
)

print(
    "Blood Pressure: "
    f"{result.get('blood_pressure')}"
)

print(
    "Physical Activity: "
    f"{result.get('physical_activity')}"
)

print("=" * 40)