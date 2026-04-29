from google.genai import types

from app.core.config import settings
from app.models.ai_diagram_models import (
    DiagramAiResponse,
    DiagramInstructionRequest,
)
from app.services.gemini_client import get_gemini_client


SYSTEM_INSTRUCTION = """
Eres un asistente experto en modelado de políticas de negocio mediante diagramas de actividades organizados por calles (lanes).

Reglas:
1. Responde SOLO con JSON válido que cumpla exactamente el esquema pedido.
2. No inventes campos fuera del esquema.
3. No cambies IDs existentes sin razón.
4. Prefiere devolver operations pequeñas y seguras.
5. Si no hace falta modificar algo, devuelve operations vacías y usa notes.
6. Conserva la lógica funcional del proceso.
"""

USER_TEMPLATE = """
Instrucción del usuario:
{prompt}

Debes analizar este diagrama y responder con este esquema:

- message: resumen corto
- operations: lista de operaciones seguras para modificar el diagrama
- notes: observaciones breves
- issues: problemas detectados opcionales

Diagrama:
{diagram_json}
"""


def instruct_diagram_with_gemini(payload: DiagramInstructionRequest) -> DiagramAiResponse:
    client = get_gemini_client()

    user_prompt = USER_TEMPLATE.format(
        prompt=payload.prompt,
        diagram_json=payload.diagram.model_dump_json(indent=2)
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=DiagramAiResponse,
            temperature=0.2,
        ),
    )

    if not response.parsed:
        raise ValueError("Gemini no devolvió una respuesta estructurada válida.")

    return response.parsed