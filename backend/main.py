from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.health import router as health_router
from backend.routers.roadmap import router as roadmap_router

app = FastAPI(title="course_recommendation_api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(roadmap_router)
