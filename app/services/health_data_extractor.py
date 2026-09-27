import re


class HealthDataExtractor:

    def extract(self, text: str) -> dict:
        data = {}

        bmi_match = re.search(
            r"\bBMI\s*[:=]\s*(\d+(?:\.\d+)?)",
            text,
            re.IGNORECASE
        )

        if bmi_match:
            data["bmi"] = float(bmi_match.group(1))

        heart_rate_match = re.search(
            r"\b(?:Heart\s*Rate|HR)\s*[:=]\s*(\d+)",
            text,
            re.IGNORECASE
        )

        if heart_rate_match:
            data["heart_rate"] = int(
                heart_rate_match.group(1)
            )

        blood_pressure_match = re.search(
            r"\b(?:Blood\s*Pressure|BP)\s*[:=]\s*(\d+)\s*/\s*(\d+)",
            text,
            re.IGNORECASE
        )

        if blood_pressure_match:
            data["blood_pressure"] = {
                "systolic": int(
                    blood_pressure_match.group(1)
                ),
                "diastolic": int(
                    blood_pressure_match.group(2)
                )
            }

        activity_match = re.search(
            r"\bPhysical\s*Activity\s*[:=]\s*(.+)",
            text,
            re.IGNORECASE
        )

        if activity_match:
            data["physical_activity"] = (
                activity_match.group(1)
                .strip()
                .splitlines()[0]
            )

        return data


health_data_extractor = HealthDataExtractor()