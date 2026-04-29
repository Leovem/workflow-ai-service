from typing import Literal
from pydantic import BaseModel, Field


DiagramNodeType = Literal[
    "lane",
    "initial",
    "action",
    "decision",
    "sync",
    "activityFinal",
    "flowFinal",
    "link",
]


class AiDiagramNode(BaseModel):
    id: str
    type: DiagramNodeType
    label: str | None = None
    laneId: str | None = None
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None
    rawType: str | None = None


class AiDiagramEdge(BaseModel):
    id: str
    type: Literal["link"] = "link"
    sourceId: str
    targetId: str
    label: str | None = None


class AiDiagramPayload(BaseModel):
    nodes: list[AiDiagramNode] = Field(default_factory=list)
    edges: list[AiDiagramEdge] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class DiagramInstructionRequest(BaseModel):
    prompt: str = Field(min_length=1)
    diagram: AiDiagramPayload


class DiagramOperation(BaseModel):
    type: Literal[
        "move_node",
        "rename_node",
        "add_node",
        "remove_node",
        "create_link",
        "remove_link",
        "assign_lane",
        "normalize_layout",
    ]
    node_id: str | None = None
    source_id: str | None = None
    target_id: str | None = None
    lane_id: str | None = None
    label: str | None = None
    x: float | None = None
    y: float | None = None
    node_type: str | None = None


class DiagramIssue(BaseModel):
    type: str
    severity: Literal["low", "medium", "high"]
    node_id: str | None = None
    lane_id: str | None = None
    title: str
    description: str
    recommendation: str | None = None


class DiagramAiResponse(BaseModel):
    message: str
    operations: list[DiagramOperation] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    issues: list[DiagramIssue] = Field(default_factory=list)