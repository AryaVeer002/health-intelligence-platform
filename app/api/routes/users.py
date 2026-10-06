from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.models.health_profile import HealthProfile
from app.models.health_record import HealthRecord
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.health import (
    HealthProfileCreate,
    HealthProfileResponse,
    HealthRecordCreate,
    HealthRecordResponse
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    statement = select(User).where(User.id == user_id)

    result = db.execute(statement)

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this user's data"
        )

    return user

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    statement = select(User).where(User.id == user_id)

    result = db.execute(statement)

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this user's data"
        )

    if user_data.name is not None:
        user.name = user_data.name

    db.commit()
    db.refresh(user)

    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    statement = select(User).where(User.id == user_id)

    result = db.execute(statement)

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this user"
        )

    user.is_deleted = True
    user.deleted_at = datetime.utcnow()

    db.commit()

    return None


@router.post(
    "/{user_id}/health-profile",
    response_model=HealthProfileResponse,
    status_code=201,
)
def create_health_profile(
    user_id: int,
    profile_data: HealthProfileCreate,
    current_user: User = Depends(get_current_user),
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

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this user's health profile"
        )

    profile_statement = select(HealthProfile).where(
        HealthProfile.user_id == user_id
    )
    profile_result = db.execute(profile_statement)
    existing_profile = profile_result.scalar_one_or_none()

    if existing_profile is not None:
        raise HTTPException(
            status_code=409,
            detail="Health profile already exists"
        )

    profile = HealthProfile(
        user_id=user_id,
        age=profile_data.age,
        weight=profile_data.weight,
        height=profile_data.height
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile



@router.post(
    "/{user_id}/health-records",
    response_model=HealthRecordResponse,
    status_code=201,
)
def create_health_record(
    user_id: int,
    record_data: HealthRecordCreate,
    current_user: User = Depends(get_current_user),
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

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this user's health records"
        )

    record = HealthRecord(
        user_id=user_id,
        record_date=record_data.record_date,
        weight=record_data.weight,
        height=record_data.height,
        heart_rate=record_data.heart_rate
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get(
    "/{user_id}/health-records",
    response_model=list[HealthRecordResponse],
)
def get_health_records(
    user_id: int,
    current_user: User = Depends(get_current_user),
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

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this user's health records"
        )

    records_statement = (
        select(HealthRecord)
        .where(HealthRecord.user_id == user_id)
        .order_by(HealthRecord.record_date.asc())
    )

    records_result = db.execute(records_statement)

    return records_result.scalars().all()