class InsightService:

    def build_trend_insights(
        self,
        grouped_measurements: dict
    ) -> list[dict]:
        insights = []

        for metric, metric_measurements in (
            grouped_measurements.items()
        ):
            if len(metric_measurements) < 2:
                continue

            first_measurement = metric_measurements[0]
            latest_measurement = metric_measurements[-1]

            first_value = first_measurement.value
            latest_value = latest_measurement.value

            change = latest_value - first_value

            if first_value != 0:
                change_percent = (
                    change / first_value
                ) * 100
            else:
                change_percent = 0

            if change > 0:
                direction = "increased"
            elif change < 0:
                direction = "decreased"
            else:
                direction = "remained stable"

            if direction == "remained stable":
                message = (
                    f"{metric} remained stable at "
                    f"{latest_value} "
                    f"{latest_measurement.unit}."
                )
            else:
                message = (
                    f"{metric} {direction} from "
                    f"{first_value} to {latest_value} "
                    f"{latest_measurement.unit} "
                    f"({abs(change_percent):.2f}% change)."
                )

            insights.append(
                {
                    "type": "trend",
                    "metric": metric,
                    "message": message
                }
            )

        return insights

    def build_anomaly_insights(
        self,
        grouped_measurements: dict
    ) -> list[dict]:
        insights = []

        for metric, metric_measurements in (
            grouped_measurements.items()
        ):
            if len(metric_measurements) < 2:
                continue

            previous_measurement = (
                metric_measurements[-2]
            )

            latest_measurement = (
                metric_measurements[-1]
            )

            previous_value = previous_measurement.value
            latest_value = latest_measurement.value

            change = latest_value - previous_value

            if previous_value != 0:
                change_percent = (
                    change / previous_value
                ) * 100
            else:
                change_percent = 0

            is_anomaly = abs(change_percent) >= 10

            if not is_anomaly:
                continue

            if change > 0:
                direction = "increased"
            elif change < 0:
                direction = "decreased"
            else:
                direction = "remained stable"

            message = (
                f"{metric} {direction} from "
                f"{previous_value} to {latest_value} "
                f"{latest_measurement.unit} "
                f"({abs(change_percent):.2f}% change)."
            )

            insights.append(
                {
                    "type": "anomaly",
                    "metric": metric,
                    "message": message
                }
            )

        return insights


insight_service = InsightService()