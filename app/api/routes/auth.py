from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserRegister
from app.services.auth_service import hash_password, verify_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    statement = select(User).where(
        User.email == user_data.email
    )

    result = db.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user_data.password
    )

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "message": "User registered successfully"
    }


@router.post("/login", response_model=TokenResponse)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    statement = select(User).where(
        User.email == user_data.email
    )

    result = db.execute(statement)
    user = result.scalar_one_or_none()

    if (
        user is None
        or user.password_hash is None
        or user.is_deleted
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    token_payload = {
        "sub": str(user.id),
        "exp": expires_at
    }

    access_token = jwt.encode(
        token_payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )