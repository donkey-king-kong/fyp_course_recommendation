from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.curriculum import router as curriculum_router
from backend.routers.faculties import router as faculties_router
from backend.routers.health import router as health_router
from backend.routers.modules import router as modules_router
from backend.routers.recommendations import router as recommendations_router
from backend.routers.roadmap import router as roadmap_router
from backend.routers.transcript import router as transcript_router

app = FastAPI(
    title="NTU Course Recommendation API",
    description=(
        "Backend API for the NTU course recommendation rebuild. Use `/modules` "
        "to browse seeded module data from PostgreSQL without loading the full "
        "dataset into the frontend."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173", "http://127.0.0.1:5174", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(roadmap_router)
app.include_router(transcript_router)
app.include_router(curriculum_router)
app.include_router(faculties_router)
app.include_router(modules_router)
app.include_router(recommendations_router)
