from typing import Any, TypedDict
from pydantic import BaseModel, Field


class FactorieState(TypedDict, total=False):
    # Entrada y salida general
    task: str
    source: str
    response: str

    # Etapa 1: Validación de tarea y Spec Writer
    task_valid: bool
    task_category: str
    validation_reason: str
    spec: dict[str, Any]
    spec_markdown: str

    # Etapa 2: Builder
    builder_status: str
    code_artifacts: list[dict[str, Any]]
    project_dir: str

    # Bucle de Auditoría, Testing y Auto-Reparación (Self-Healing Loop)
    build_attempts: int
    max_build_attempts: int
    last_error: str
    error_file: str
    audit_passed: bool
    audit_report: dict[str, Any]
    project_memory: list[str]

    # Etapa 3: Subagents (Seguridad, UI, Código, Arquitectura)
    subagents_reviews: dict[str, Any]

    # Etapa 4: Approver
    approved: bool
    approval_notes: str

    # Etapa 5: Human in the loop
    human_feedback: str
    human_approved: bool


class TaskRequest(BaseModel):
    description: str = Field(min_length=1)
    source: str = "unknown"


class TaskResult(BaseModel):
    response: str
