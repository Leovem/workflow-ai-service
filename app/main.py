from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.health import router as health_router
from app.routers.ai_diagram import router as ai_diagram_router
from app.routers.ai_workflow_forms import router as ai_workflow_forms_router

app = FastAPI(
    title="Workflow AI Service",
    version="1.0.0",
    description="Servicio IA para edición, normalización y generación de formularios de workflows"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(ai_diagram_router)
app.include_router(ai_workflow_forms_router)