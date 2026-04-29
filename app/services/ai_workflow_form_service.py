from google.genai import types

from app.core.config import settings
from app.models.ai_workflow_form_models import (
    GenerateWorkflowFormsRequest,
    GenerateWorkflowFormsResponse,
)
from app.services.gemini_client import get_gemini_client


SYSTEM_INSTRUCTION = """
Eres un asistente experto en modelado de workflows, políticas de negocio y generación de formularios dinámicos.

Tu tarea es generar formularios para actividades de un diagrama de actividades organizado por calles/departamentos.

Reglas estrictas:
1. Responde SOLO con JSON válido que cumpla exactamente el esquema pedido.
2. No incluyas explicaciones fuera del JSON.
3. Genera exactamente un formulario por cada actividad recibida.
4. Usa el nodeId exacto de cada actividad.
5. No inventes nodeIds.
6. No cambies IDs existentes.
7. No inventes datos personales sensibles.
8. Usa campos genéricos reutilizables para cualquier tipo de empresa.
9. Cada formulario debe tener mínimo 2 campos y máximo 6 campos.
10. Usa solamente estos tipos de campo:
    text, textarea, number, date, select, checkbox, file, image.
11. Si una actividad permite aprobar o rechazar, agrega un campo select llamado "Resultado".
12. Si una actividad permite rechazar, agrega un campo "Observaciones".
13. Si una actividad requiere adjunto, agrega un campo file.
14. Si una actividad parece inspección, verificación física o revisión visual, agrega un campo image opcional.
15. Si no estás seguro, genera campos mínimos: Resultado, Observaciones y Evidencia.
16. El formulario debe servir para que un funcionario registre el trabajo realizado en esa actividad.
"""

USER_TEMPLATE = """
Genera formularios dinámicos para TODAS las actividades del siguiente workflow.

Debes devolver este esquema:
- forms: lista de formularios generados
  - nodeId: id exacto de la actividad
  - title: título del formulario
  - description: descripción corta
  - fields: campos del formulario
    - label
    - type
    - required
    - placeholder
    - options

Contexto del workflow:
{context_json}
"""


def generate_workflow_forms_with_gemini(
    payload: GenerateWorkflowFormsRequest,
) -> GenerateWorkflowFormsResponse:
    client = get_gemini_client()

    user_prompt = USER_TEMPLATE.format(
        context_json=payload.context.model_dump_json(indent=2)
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=GenerateWorkflowFormsResponse,
            temperature=0.2,
        ),
    )

    if not response.parsed:
        raise ValueError("Gemini no devolvió formularios estructurados válidos.")

    parsed: GenerateWorkflowFormsResponse = response.parsed

    expected_node_ids = {activity.nodeId for activity in payload.context.activities}
    received_node_ids = {form.nodeId for form in parsed.forms}

    missing_node_ids = expected_node_ids - received_node_ids
    invalid_node_ids = received_node_ids - expected_node_ids

    if invalid_node_ids:
        raise ValueError(
            f"Gemini devolvió formularios con nodeId inválido: {sorted(invalid_node_ids)}"
        )

    if missing_node_ids:
        raise ValueError(
            f"Gemini no generó formularios para estas actividades: {sorted(missing_node_ids)}"
        )

    return parsed