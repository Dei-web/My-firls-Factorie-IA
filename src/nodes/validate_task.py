from domain.spec import TaskValidation
from domain.state import FactorieState
from factorie_ia.core.models_ia.nemotron import build_nemotron


def validate_task(state: FactorieState) -> dict:
    """Valida si la entrada del usuario corresponde a una solicitud de desarrollo web.

    Filtra saludos, texto ambiguo o peticiones ajenas a la creación de software.
    """
    model = build_nemotron().with_structured_output(TaskValidation)

    result: TaskValidation = model.invoke(
        [
            (
                "system",
                """
Eres el filtro inicial y clasificador de Factorie-Ia, una factoría autónoma de desarrollo web.

Tu responsabilidad es determinar si el mensaje del usuario representa una intención o solicitud
de creación, desarrollo, diseño o modificación de una página web, landing page o aplicación de software.

Reglas:
1. Si el usuario pide crear una web (ej: "generame un web de pintura", "quiero una landing page para abogados", "hazme una tienda online"),
   marca is_valid_task = True, clasifica la categoría (ej: 'portfolio', 'landing_page', 'ecommerce', etc.) y resume la intención.
2. Si el mensaje es solo un saludo (ej: "hola", "buenas"), texto aleatorio sin sentido (ej: "asdfgh"), o algo ajeno al desarrollo web,
   marca is_valid_task = False y explica con amabilidad qué tipo de proyectos web puede solicitar.
3. No desarrolles la web ni la especificación en este paso. Solo valida y clasifica.
""",
            ),
            ("human", state["task"]),
        ]
    )

    updates = {
        "task_valid": result.is_valid_task,
        "task_category": result.task_category,
        "validation_reason": result.reason,
    }

    if not result.is_valid_task:
        updates["response"] = (
            f"⚠️ **Solicitud no identificada como tarea web**\n\n"
            f"{result.reason}\n\n"
            f"💡 *Ejemplo:* 'Generame una web de pintura para un artista independiente'."
        )

    return updates
