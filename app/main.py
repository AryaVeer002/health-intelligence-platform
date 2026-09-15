from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Health Intelligence Platform API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "health-intelligence-platform"
    }