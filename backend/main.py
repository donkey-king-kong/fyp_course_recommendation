from fastapi import FastAPI

from backend.routers.health import router as health_router

app = FastAPI(title="course_recommendation_api")

app.include_router(health_router)
