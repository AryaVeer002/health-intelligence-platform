from fastapi import APIRouter

from app.schemas.health import HealthProfile


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "health-intelligence-platform"
    }


@router.post("/health/profile")
def create_health_profile(profile: HealthProfile):
    return {
        "message": "Health profile received",
        "profile": profile
    }