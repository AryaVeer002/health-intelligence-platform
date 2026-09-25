from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.user import User
from app.models.health_record import HealthRecord

from app.schemas.analytics import (
    TrendResponse,
    AnomalyResponse,
    RiskResponse,
    RiskAssessmentRequest,
)

from app.services.risk_service import risk_service


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
            "BMI",
            "Age group",
            "General health",
            "Physical health",
            "Physical activity",
            "Smoking",
            "Alcohol",
            "Sex",
        ],
    }