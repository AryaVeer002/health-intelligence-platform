from fastapi import APIRouter


router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"]
)


@router.get("/test")
def assistant_test():
    return {
        "message": "Assistant API is working"
    }