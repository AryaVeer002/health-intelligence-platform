from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.user import User
from app.models.health_record import HealthRecord
from app.schemas.analytics import TrendResponse


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