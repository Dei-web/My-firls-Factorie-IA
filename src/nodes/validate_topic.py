from domain.diagram import TopicValidation
from factorie_ia.core.models_ia.nemotron import build_nemotron
from domain.state import FactorieState


def validate_topic(state: FactorieState) -> dict:
    model = build_nemotron().with_structured_output(TopicValidation)

    result = model.invoke(
        [
            (
                "system",
                """
            Eres un validador de temas para diagramas Mermaid.

            Determina si el tema del usuario es suficientemente claro
            y adecuado para representar conceptos, procesos,
            componentes o relaciones mediante un diagrama.

            Si es ambiguo, irrelevante o insuficiente, marca valid=False
            y explica brevemente qué falta.

            No generes el diagrama en esta etapa.
            """,
            ),
            ("human", state["task"]),
        ]
    )

    updates = {
        "topic_valid": result.valid,
        "normalized_topic": result.normalized_topic,
        "validation_reason": result.reason,
    }

    if not result.valid:
        updates["response"] = result.reason

    return updates
