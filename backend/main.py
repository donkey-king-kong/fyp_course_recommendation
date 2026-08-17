from fastapi import FastAPI

from backend.routers.health import router as health_router
from backend.routers.roadmap import router as roadmap_router

app = FastAPI(title="course_recommendation_api")

app.include_router(health_router)
app.include_router(roadmap_router)
