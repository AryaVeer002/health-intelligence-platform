class BMIService:

    def calculate(
        self,
        weight_kg: float,
        height_cm: float
    ) -> float:
        if weight_kg <= 0:
            raise ValueError(
                "Weight must be greater than zero"
            )

        if height_cm <= 0:
            raise ValueError(
                "Height must be greater than zero"
            )

        height_m = height_cm / 100

        bmi = weight_kg / (height_m ** 2)

        return round(bmi, 2)


bmi_service = BMIService()