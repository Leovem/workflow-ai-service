from app.models.diagram_models import DiagramPayload

def normalize_diagram(diagram: DiagramPayload) -> tuple[DiagramPayload, list[str]]:
    changes: list[str] = []

    # 1. ordenar nodos por lane y luego por posición vertical/horizontal
    diagram.nodes.sort(
        key=lambda n: (
            n.lane_id or "",
            n.y if n.y is not None else 0,
            n.x if n.x is not None else 0,
        )
    )
    changes.append("Se ordenaron los nodos por lane y posición.")

    # 2. limpiar labels vacíos
    for node in diagram.nodes:
        if node.label is not None:
            clean = node.label.strip()
            if clean != node.label:
                node.label = clean
                changes.append(f"Se limpió el label del nodo {node.id}.")

    # 3. asegurar metadata
    if diagram.metadata is None:
        diagram.metadata = {}
        changes.append("Se inicializó metadata del diagrama.")

    return diagram, changes