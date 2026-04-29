from fastapi import APIRouter, HTTPException

from app.models.ai_workflow_form_models import (
    GenerateWorkflowFormsRequest,
    GenerateWorkflowFormsResponse,
)
from app.services.ai_workflow_form_service import (
    generate_workflow_forms_with_gemini,
)

router = APIRouter(
    prefix="/ai/workflow/forms",
    tags=["AI Workflow Forms"],
)


@router.post("/generate", response_model=GenerateWorkflowFormsResponse)
def generate_workflow_forms(
    payload: GenerateWorkflowFormsRequest,
) -> GenerateWorkflowFormsResponse:
    try:
        return generate_workflow_forms_with_gemini(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Error interno al generar formularios con IA.",
        ) from exc