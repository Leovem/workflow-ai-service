from fastapi import APIRouter, HTTPException

from app.models.ai_diagram_models import (
    DiagramAiResponse,
    DiagramInstructionRequest,
)
from app.services.diagram_ai_service import instruct_diagram_with_gemini

router = APIRouter(prefix="/ai/diagram", tags=["ai-diagram"])


@router.post("/instruct", response_model=DiagramAiResponse)
def instruct_diagram(payload: DiagramInstructionRequest):
    try:
        return instruct_diagram_with_gemini(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc