from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.auth.settings import AUTH0_SECRET
from backend.dependencies.auth import require_user
from backend.routers.auth import router as auth_router
from backend.routers.curriculum import router as curriculum_router
from backend.routers.faculties import router as faculties_router
from backend.routers.health import router as health_router
from backend.routers.modules import router as modules_router
from backend.routers.recommendations import router as recommendations_router
from backend.routers.roadmap import router as roadmap_router
from backend.routers.roadmap_readiness import router as roadmap_readiness_router
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

# SessionMiddleware must be added before CORS so the session cookie is set correctly.
app.add_middleware(
    SessionMiddleware,
    secret_key=AUTH0_SECRET,
    same_site="lax",
    https_only=False,
    max_age=8 * 60 * 60,  # 8 hours
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173", "http://127.0.0.1:5174", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth routes are public (no require_user dependency).
app.include_router(auth_router)
app.include_router(health_router)

# All data routes require an active session.
_auth = [Depends(require_user)]
app.include_router(roadmap_router, dependencies=_auth)
app.include_router(roadmap_readiness_router, dependencies=_auth)
app.include_router(transcript_router, dependencies=_auth)
app.include_router(curriculum_router, dependencies=_auth)
app.include_router(faculties_router, dependencies=_auth)
app.include_router(modules_router, dependencies=_auth)
app.include_router(recommendations_router, dependencies=_auth)
