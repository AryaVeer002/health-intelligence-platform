from fastapi import APIRouter


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/test")
def analytics_test():
    return {
        "message": "Analytics API is working"
    }