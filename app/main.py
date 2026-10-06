from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.reports import router as reports_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.assistant import router as assistant_router



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    users_router,
    prefix="/api/v1"
)

app.include_router(
    reports_router,
    prefix="/api/v1"
)

app.include_router(
    analytics_router,
    prefix="/api/v1"
)

app.include_router(
    assistant_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {
        "message": "Health Intelligence Platform API is running"
    }