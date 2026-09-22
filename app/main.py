from fastapi import FastAPI

from app.api.routes.health import router as health_router


app = FastAPI()


app.include_router(
    health_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "Health Intelligence Platform API is running"
    }