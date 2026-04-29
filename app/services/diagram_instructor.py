from app.models.diagram_models import DiagramPayload

def apply_instruction(prompt: str, diagram: DiagramPayload) -> tuple[DiagramPayload, list[str]]:
    text = prompt.lower().strip()
    changes: list[str] = []

    if "orden" in text or "organiza" in text:
        diagram.nodes.sort(
            key=lambda n: (
                n.lane_id or "",
                n.y if n.y is not None else 0,
                n.x if n.x is not None else 0,
            )
        )
        changes.append("Se reorganizó el diagrama por calles y posición.")

    if "renombra" in text:
        changes.append("La instrucción de renombrado fue detectada, pero aún no está implementada.")

    if not changes:
        changes.append("No se aplicaron cambios automáticos; la instrucción quedó registrada.")

    return diagram, changes