from pathlib import Path

from app.services.report_extractor import report_extractor


file_path = Path("data/reports/test_report.txt")

text = report_extractor.extract_text(file_path)

print()
print("=" * 40)
print("REPORT EXTRACTION TEST")
print("=" * 40)
print(text)
print("=" * 40)