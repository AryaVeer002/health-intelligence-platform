from fastapi import APIRouter


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/test")
def reports_test():
    return {
        "message": "Reports API is working"
    }