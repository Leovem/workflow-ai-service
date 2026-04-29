from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.routers.health import router as health_router
from app.routers.ai_diagram import router as ai_diagram_router
from app.routers.ai_workflow_forms import router as ai_workflow_forms_router


app = FastAPI(
    title="Workflow AI Service",
    version="1.0.0",
    description="Servicio IA para edición, normalización y generación de formularios de workflows"
)


allowed_origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://frontend-workflow-seven.vercel.app",
    settings.frontend_url,
]

allowed_origins = list({
    origin.strip().rstrip("/")
    for origin in allowed_origins
    if origin and origin.strip()
})


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/debug/cors")
def debug_cors():
    return {
        "frontend_url": settings.frontend_url,
        "allowed_origins": allowed_origins,
        "environment": settings.environment,
    }


app.include_router(health_router)
app.include_router(ai_diagram_router)
app.include_router(ai_workflow_forms_router)