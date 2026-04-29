from typing import Any, Literal
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


class DiagramNode(BaseModel):
    id: str
    type: DiagramNodeType
    label: str | None = None
    lane_id: str | None = None
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DiagramEdge(BaseModel):
    id: str
    type: Literal["link"] = "link"
    source_id: str
    target_id: str
    label: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DiagramPayload(BaseModel):
    nodes: list[DiagramNode] = Field(default_factory=list)
    edges: list[DiagramEdge] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)