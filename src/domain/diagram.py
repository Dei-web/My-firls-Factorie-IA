from pydantic import BaseModel, Field


class TopicValidation(BaseModel):
    valid: bool = Field(
        description="Indica si el tema es adecuado para crear un diagrama Mermaid."
    )
    normalized_topic: str = Field(
        description="Tema concreto y claro que se utilizará como referencia."
    )
    reason: str = Field(description="Motivo de la decisión de validación.")


class MermaidDiagram(BaseModel):
    title: str = Field(description="Título del diagrama.")
    description: str = Field(description="Descripción breve del diagrama.")
    mermaid: str = Field(
        description="Código Mermaid válido, sin bloques Markdown ni explicaciones."
    )
