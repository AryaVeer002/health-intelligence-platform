from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.user import User
from app.models.risk_profile import RiskProfile
from app.models.health_profile import HealthProfile
from app.schemas.health import (
    HealthProfileCreate,
    HealthProfileResponse,
    RiskProfileCreate,
    RiskProfileResponse,
)

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "health-intelligence-platform"
    }


@router.post(
    "/health/profile/{user_id}",
    response_model=HealthProfileResponse
)
def create_health_profile(
    user_id: int,
    profile: HealthProfileCreate,
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

    existing_statement = select(
        HealthProfile
    ).where(
        HealthProfile.user_id == user_id
    )

    existing_result = db.execute(
        existing_statement
    )

    existing_profile = (
        existing_result.scalar_one_or_none()
    )

    if existing_profile is not None:
        raise HTTPException(
            status_code=409,
            detail="Health profile already exists"
        )

    health_profile = HealthProfile(
        user_id=user_id,
        age=profile.age,
        weight=profile.weight,
        height=profile.height
    )

    db.add(health_profile)
    db.commit()
    db.refresh(health_profile)

    return health_profile




@router.post(
    "/health/risk-profile/{user_id}",
    response_model=RiskProfileResponse
)
def create_risk_profile(
    user_id: int,
    profile: RiskProfileCreate,
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

    existing_statement = select(
        RiskProfile
    ).where(
        RiskProfile.user_id == user_id
    )

    existing_result = db.execute(
        existing_statement
    )

    existing_profile = (
        existing_result.scalar_one_or_none()
    )

    if existing_profile is not None:
        raise HTTPException(
            status_code=409,
            detail="Risk profile already exists"
        )

    risk_profile = RiskProfile(
        user_id=user_id,
        sex=profile.sex,
        general_health=profile.general_health,
        physical_health_days=profile.physical_health_days,
        physical_activity=profile.physical_activity,
        smoking=profile.smoking,
        alcohol=profile.alcohol
    )

    db.add(risk_profile)
    db.commit()
    db.refresh(risk_profile)

    return risk_profile