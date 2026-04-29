import traceback

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
        print("ERROR DE VALIDACIÓN AL GENERAR FORMULARIOS IA")
        print(type(exc).__name__)
        print(str(exc))
        traceback.print_exc()

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        print("ERROR INTERNO AL GENERAR FORMULARIOS IA")
        print(type(exc).__name__)
        print(str(exc))
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Error interno al generar formularios con IA: {type(exc).__name__}: {str(exc)}",
        ) from exc