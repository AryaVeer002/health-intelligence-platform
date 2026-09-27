from app.models.health_profile import HealthProfile
from app.models.risk_profile import RiskProfile
from app.services.bmi_service import bmi_service


class RiskFeatureService:

    def build_features(
        self,
        health_profile: HealthProfile,
        risk_profile: RiskProfile
    ) -> dict:

        bmi = bmi_service.calculate(
            health_profile.weight,
            health_profile.height
        )

        age_group = self._get_age_group(
            health_profile.age
        )

        return {
            "_BMI5": bmi,
            "_AGEG5YR": age_group,
            "SEX": risk_profile.sex,
            "_RFHLTH": risk_profile.general_health,
            "PHYSHLTH": risk_profile.physical_health_days,
            "_TOTINDA": risk_profile.physical_activity,
            "_RFSMOK3": risk_profile.smoking,
            "DRNKANY5": risk_profile.alcohol,
        }

    def _get_age_group(self, age: int) -> int:
        if age < 25:
            return 1
        elif age < 30:
            return 2
        elif age < 35:
            return 3
        elif age < 40:
            return 4
        elif age < 45:
            return 5
        elif age < 50:
            return 6
        elif age < 55:
            return 7
        elif age < 60:
            return 8
        elif age < 65:
            return 9
        elif age < 70:
            return 10
        elif age < 75:
            return 11
        elif age < 80:
            return 12
        elif age < 85:
            return 13
        else:
            return 14


risk_feature_service = RiskFeatureService()