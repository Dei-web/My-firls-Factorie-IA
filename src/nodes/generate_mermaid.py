from domain.diagram import MermaidDiagram
from domain.state import FactorieState
from factorie_ia.core.models_ia.nemotron import build_nemotron


def generate_mermaid(state: FactorieState) -> dict:
    model = build_nemotron().with_structured_output(MermaidDiagram)

    result = model.invoke(
        [
            (
                "system",
                """
            Eres un especialista en diagramas Mermaid.

            Genera un diagrama correcto y coherente con el tema recibido.
            Elige el tipo de diagrama Mermaid más apropiado.
            Usa sintaxis Mermaid válida.
            No incluyas bloques Markdown ni explicaciones dentro del campo mermaid.
            No inventes detalles específicos que el usuario no haya proporcionado.
            """,
            ),
            (
                "human",
                f"Tema: {state['normalized_topic']}",
            ),
        ]
    )

    response_content = (
        f"📊 {result.title}\n\n"
        f"{result.description}\n\n"
        f"```mermaid\n{result.mermaid}\n```"
    )

    return {
        "diagram_title": result.title,
        "diagram_description": result.description,
        "mermaid": result.mermaid,
        "response": response_content,
    }
