from typing import Literal

from pydantic import BaseModel, Field


WorkflowFormFieldType = Literal[
    "text",
    "textarea",
    "number",
    "date",
    "select",
    "checkbox",
    "file",
    "image",
]


class WorkflowAIContextDepartment(BaseModel):
    id: str
    name: str
    description: str | None = None


class WorkflowAIContextActivity(BaseModel):
    nodeId: str
    label: str
    departmentId: str | None = None
    departmentName: str | None = None
    description: str | None = None
    businessConfig: dict | None = None


class WorkflowAIContextDecision(BaseModel):
    nodeId: str
    label: str


class WorkflowAIContextTransition(BaseModel):
    sourceId: str
    targetId: str
    label: str | None = None


class WorkflowAIContext(BaseModel):
    processName: str
    departments: list[WorkflowAIContextDepartment] = Field(default_factory=list)
    activities: list[WorkflowAIContextActivity] = Field(default_factory=list)
    decisions: list[WorkflowAIContextDecision] = Field(default_factory=list)
    transitions: list[WorkflowAIContextTransition] = Field(default_factory=list)


class GenerateWorkflowFormsRequest(BaseModel):
    context: WorkflowAIContext


class AIGeneratedWorkflowFormField(BaseModel):
    label: str
    type: WorkflowFormFieldType
    required: bool
    placeholder: str | None = None
    options: list[str] = Field(default_factory=list)


class AIGeneratedWorkflowForm(BaseModel):
    nodeId: str
    title: str
    description: str | None = None
    fields: list[AIGeneratedWorkflowFormField] = Field(default_factory=list)


class GenerateWorkflowFormsResponse(BaseModel):
    forms: list[AIGeneratedWorkflowForm] = Field(default_factory=list)