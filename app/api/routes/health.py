from fastapi import APIRouter

from app.schemas.health import HealthProfileCreate

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "health-intelligence-platform"
    }


@router.post("/health/profile")
def create_health_profile(profile: HealthProfileCreate):
    return {
        "message": "Health profile received",
        "profile": profile
    }