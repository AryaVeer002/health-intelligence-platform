from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.models.user import User
from app.models.health_record import HealthRecord
from app.models.health_profile import HealthProfile
from app.models.risk_profile import RiskProfile
from app.models.health_measurement import HealthMeasurement

from app.schemas.analytics import (
    TrendResponse,
    AnomalyResponse,
    RiskResponse,
    RiskAssessmentRequest,
)

from app.services.bmi_service import bmi_service
from app.services.insight_service import insight_service
from app.services.risk_service import risk_service
from app.services.risk_feature_service import risk_feature_service

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/test")
def analytics_test():
    return {
        "message": "Analytics API is working"
    }


@router.get(
    "/users/{user_id}/weight-trend",
    response_model=TrendResponse
)
def get_weight_trend(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(User.id == user_id)
    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    records_statement = (
        select(HealthRecord)
        .where(HealthRecord.user_id == user_id)
        .order_by(HealthRecord.record_date.asc())
    )

    records_result = db.execute(records_statement)
    records = records_result.scalars().all()

    if len(records) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two health records are required"
        )

    start_value = records[0].weight
    end_value = records[-1].weight
    change = end_value - start_value

    if change > 0:
        direction = "increasing"
    elif change < 0:
        direction = "decreasing"
    else:
        direction = "stable"

    return {
        "metric": "weight",
        "start_value": start_value,
        "end_value": end_value,
        "change": change,
        "direction": direction
    }


@router.get(
    "/users/{user_id}/heart-rate-anomalies",
    response_model=list[AnomalyResponse]
)
def get_heart_rate_anomalies(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(User.id == user_id)
    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    records_statement = (
        select(HealthRecord)
        .where(HealthRecord.user_id == user_id)
        .order_by(HealthRecord.record_date.asc())
    )

    records_result = db.execute(records_statement)
    records = records_result.scalars().all()

    if len(records) < 3:
        raise HTTPException(
            status_code=400,
            detail="At least three health records are required"
        )

    anomalies = []
    historical_values = []

    for record in records:
        if historical_values:
            expected_value = (
                sum(historical_values) / len(historical_values)
            )

            difference = abs(
                record.heart_rate - expected_value
            )

            if difference >= 20:
                severity = "high"
            elif difference >= 10:
                severity = "moderate"
            else:
                severity = None

            if severity is not None:
                anomalies.append(
                    {
                        "metric": "heart_rate",
                        "value": record.heart_rate,
                        "expected_value": round(
                            expected_value,
                            2
                        ),
                        "severity": severity,
                        "detected_at": record.record_date
                    }
                )

        historical_values.append(record.heart_rate)

    return anomalies


@router.post(
    "/users/{user_id}/risk",
    response_model=RiskResponse
)
def get_health_risk(
    user_id: int,
    assessment: RiskAssessmentRequest,
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(User.id == user_id)
    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    model_features = {
        "_BMI5": assessment.bmi,
        "_AGEG5YR": assessment.age_group,
        "SEX": assessment.sex,
        "_RFHLTH": assessment.general_health,
        "PHYSHLTH": assessment.physical_health_days,
        "_TOTINDA": assessment.physical_activity,
        "_RFSMOK3": assessment.smoking,
        "DRNKANY5": assessment.alcohol,
    }

    prediction = risk_service.predict(model_features)

    return {
        "risk_type": "diabetes",
        "risk_score": round(
            prediction["risk_score"],
            4
        ),
        "risk_level": prediction["risk_level"],
        "contributing_factors": [
            item["factor"]
            for item in prediction["explanations"]
        ],
        "explanations": prediction["explanations"],
    }



@router.get("/users/{user_id}/measurements")
def get_user_measurements(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(
        User.id == user_id
    )

    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    measurement_statement = (
        select(HealthMeasurement)
        .where(
            HealthMeasurement.user_id == user_id
        )
        .order_by(
            HealthMeasurement.measured_at.asc()
        )
    )

    measurement_result = db.execute(
        measurement_statement
    )

    measurements = (
        measurement_result.scalars().all()
    )

    return {
        "user_id": user_id,
        "count": len(measurements),
        "measurements": [
            {
                "id": measurement.id,
                "metric": measurement.metric,
                "value": measurement.value,
                "unit": measurement.unit,
                "measured_at": measurement.measured_at,
                "report_id": measurement.report_id
            }
            for measurement in measurements
        ]
    }   


@router.get("/users/{user_id}/trends")
def get_user_trends(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(
        User.id == user_id
    )

    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    measurement_statement = (
        select(HealthMeasurement)
        .where(
            HealthMeasurement.user_id == user_id
        )
        .order_by(
            HealthMeasurement.measured_at.asc()
        )
    )

    measurement_result = db.execute(
        measurement_statement
    )

    measurements = (
        measurement_result.scalars().all()
    )

    grouped_measurements = {}

    for measurement in measurements:
        metric = measurement.metric

        if metric not in grouped_measurements:
            grouped_measurements[metric] = []

        grouped_measurements[metric].append(
            measurement
        )

    trends = []

    for metric, metric_measurements in (
        grouped_measurements.items()
    ):
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
            trend = "increasing"
        elif change < 0:
            trend = "decreasing"
        else:
            trend = "stable"

        trends.append(
            {
                "metric": metric,
                "unit": latest_measurement.unit,
                "first_value": first_value,
                "latest_value": latest_value,
                "change": round(change, 2),
                "change_percent": round(
                    change_percent,
                    2
                ),
                "trend": trend,
                "measurement_count": len(
                    metric_measurements
                ),
                "first_measured_at":
                    first_measurement.measured_at,
                "latest_measured_at":
                    latest_measurement.measured_at
            }
        )

    return {
        "user_id": user_id,
        "trend_count": len(trends),
        "trends": trends
    }



@router.get("/users/{user_id}/anomalies")
def get_user_anomalies(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(
        User.id == user_id
    )

    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    measurement_statement = (
        select(HealthMeasurement)
        .where(
            HealthMeasurement.user_id == user_id
        )
        .order_by(
            HealthMeasurement.measured_at.asc()
        )
    )

    measurement_result = db.execute(
        measurement_statement
    )

    measurements = (
        measurement_result.scalars().all()
    )

    grouped_measurements = {}

    for measurement in measurements:
        metric = measurement.metric

        if metric not in grouped_measurements:
            grouped_measurements[metric] = []

        grouped_measurements[metric].append(
            measurement
        )

    anomalies = []

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

        anomalies.append(
            {
                "metric": metric,
                "unit": latest_measurement.unit,
                "previous_value": previous_value,
                "latest_value": latest_value,
                "change": round(change, 2),
                "change_percent": round(
                    change_percent,
                    2
                ),
                "is_anomaly": is_anomaly,
                "measured_at":
                    latest_measurement.measured_at
            }
        )

    return {
        "user_id": user_id,
        "anomaly_count": sum(
            1
            for item in anomalies
            if item["is_anomaly"]
        ),
        "anomalies": anomalies
    }


@router.get("/users/{user_id}/insights")
def get_user_insights(
    user_id: int,
    db: Session = Depends(get_db)
):
    user_statement = select(User).where(
        User.id == user_id
    )
    profile_statement = select(
        HealthProfile
    ).where(
        HealthProfile.user_id == user_id
    )

    profile_result = db.execute(
        profile_statement
    )

    profile = profile_result.scalar_one_or_none()

    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    measurement_statement = (
        select(HealthMeasurement)
        .where(
            HealthMeasurement.user_id == user_id
        )
        .order_by(
            HealthMeasurement.measured_at.asc()
        )
    )

    measurement_result = db.execute(
        measurement_statement
    )

    measurements = (
        measurement_result.scalars().all()
    )

    grouped_measurements = {}

    for measurement in measurements:
        metric = measurement.metric

        if metric not in grouped_measurements:
            grouped_measurements[metric] = []

        grouped_measurements[metric].append(
            measurement
        )

    trend_insights = (
        insight_service.build_trend_insights(
            grouped_measurements
        )
    )

    anomaly_insights = (
        insight_service.build_anomaly_insights(
            grouped_measurements
        )
    )

    insights = trend_insights + anomaly_insights

    if profile is not None:
        bmi = bmi_service.calculate(
            profile.weight,
            profile.height
        )

        insights.append(
            {
                "type": "profile",
                "metric": "BMI",
                "message": (
                    f"Current calculated BMI is "
                    f"{bmi} kg/m²."
                )
            }
        )

        risk_statement = select(
            RiskProfile
        ).where(
            RiskProfile.user_id == user_id
        )

        risk_result = db.execute(
            risk_statement
        )

        risk_profile = (
            risk_result.scalar_one_or_none()
        )

        if profile is not None and risk_profile is not None:
            risk_features = (
                risk_feature_service.build_features(
                    profile,
                    risk_profile
                )
            )

            prediction = risk_service.predict(
                risk_features
            )

            insights.append(
                {
                    "type": "risk",
                    "metric": "Diabetes risk",
                    "risk_score": round(
                        prediction["risk_score"],
                        4
                    ),
                    "risk_level": prediction["risk_level"],
                    "message": (
                        f"Model-estimated diabetes risk "
                        f"score is "
                        f"{prediction['risk_score']:.4f} "
                        f"({prediction['risk_level']})."
                    ),
                    "explanations": (
                        prediction["explanations"]
                    )
                }
            )

    return {
        "user_id": user_id,
        "insight_count": len(insights),
        "insights": insights
    }

@router.get("/users/{user_id}/dashboard")
def get_user_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):
    # --------------------------------------------------
    # 1. Verify user
    # --------------------------------------------------

    user_statement = select(User).where(
        User.id == user_id
    )

    user_result = db.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # --------------------------------------------------
    # 2. Get health profile
    # --------------------------------------------------

    profile_statement = select(
        HealthProfile
    ).where(
        HealthProfile.user_id == user_id
    )

    profile_result = db.execute(profile_statement)
    profile = profile_result.scalar_one_or_none()

    dashboard_profile = None

    if profile is not None:
        bmi = bmi_service.calculate(
            profile.weight,
            profile.height
        )

        dashboard_profile = {
            "age": profile.age,
            "weight": profile.weight,
            "height": profile.height,
            "bmi": bmi
        }

    # --------------------------------------------------
    # 3. Get measurements
    # --------------------------------------------------

    measurement_statement = (
        select(HealthMeasurement)
        .where(
            HealthMeasurement.user_id == user_id
        )
        .order_by(
            HealthMeasurement.measured_at.asc()
        )
    )

    measurement_result = db.execute(
        measurement_statement
    )

    measurements = (
        measurement_result.scalars().all()
    )

    # --------------------------------------------------
    # 4. Group measurements
    # --------------------------------------------------

    grouped_measurements = {}

    for measurement in measurements:
        metric = measurement.metric

        if metric not in grouped_measurements:
            grouped_measurements[metric] = []

        grouped_measurements[metric].append(
            measurement
        )

    # --------------------------------------------------
    # 5. Build trends
    # --------------------------------------------------

    trends = []

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
            trend = "increasing"
        elif change < 0:
            trend = "decreasing"
        else:
            trend = "stable"

        trends.append({
            "metric": metric,
            "unit": latest_measurement.unit,
            "first_value": first_value,
            "latest_value": latest_value,
            "change": round(change, 2),
            "change_percent": round(
                change_percent,
                2
            ),
            "trend": trend
        })

    # --------------------------------------------------
    # 6. Build anomalies
    # --------------------------------------------------

    anomalies = []

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

        anomalies.append({
            "metric": metric,
            "unit": latest_measurement.unit,
            "previous_value": previous_value,
            "latest_value": latest_value,
            "change": round(change, 2),
            "change_percent": round(
                change_percent,
                2
            ),
            "is_anomaly": is_anomaly,
            "measured_at":
                latest_measurement.measured_at
        })
        
        anomalies = [
        item
        for item in anomalies
        if item["is_anomaly"]
    ]


    # --------------------------------------------------
    # 7. Build insights
    # --------------------------------------------------

    trend_insights = (
        insight_service.build_trend_insights(
            grouped_measurements
        )
    )

    anomaly_insights = (
        insight_service.build_anomaly_insights(
            grouped_measurements
        )
    )

    insights = (
        trend_insights +
        anomaly_insights
    )

    # --------------------------------------------------
    # 8. Calculate ML risk
    # --------------------------------------------------

    dashboard_risk = None

    if profile is not None:

        risk_statement = select(
            RiskProfile
        ).where(
            RiskProfile.user_id == user_id
        )

        risk_result = db.execute(
            risk_statement
        )

        risk_profile = (
            risk_result.scalar_one_or_none()
        )

        if risk_profile is not None:

            risk_features = (
                risk_feature_service.build_features(
                    profile,
                    risk_profile
                )
            )

            prediction = risk_service.predict(
                risk_features
            )

            dashboard_risk = {
                "risk_type": "diabetes",
                "risk_score": round(
                    prediction["risk_score"],
                    4
                ),
                "risk_level":
                    prediction["risk_level"],
                "explanations":
                    prediction["explanations"]
            }

            insights.append({
                "type": "risk",
                "metric": "Diabetes risk",
                "risk_score": round(
                    prediction["risk_score"],
                    4
                ),
                "risk_level":
                    prediction["risk_level"],
                "message": (
                    f"Model-estimated diabetes "
                    f"risk score is "
                    f"{prediction['risk_score']:.4f} "
                    f"({prediction['risk_level']})."
                ),
                "explanations":
                    prediction["explanations"]
            })

    # --------------------------------------------------
    # 9. Return dashboard
    # --------------------------------------------------

    return {
        "user_id": user_id,
        "profile": dashboard_profile,
        "risk": dashboard_risk,
        "trends": trends,
        "anomalies": anomalies,
        "insights": insights
    }