from langgraph.graph import StateGraph, START, END
from domain.state import FactorieState
from nodes.validate_task import validate_task
from nodes.spec_writer import spec_writer
from nodes.builder import builder_node
from nodes.auditor import auditor_node
from nodes.condicion import route_after_task_validation, route_after_audit


def build_workflow():
    """Construye y compila el flujo multi-agente autónomo de Factorie-Ia.

    Flujo:
    1. START -> validate_task (filtro y clasificador de tareas web)
    2. validate_task -> (si es válida) -> spec_writer (arquitecto de requerimientos)
                     -> (si es inválida) -> END (informa al usuario la razón)
    3. spec_writer -> builder (scaffold inicial + generación de componentes con memoria)
    4. builder -> auditor (auditoría en tiempo real con suite de pruebas 'vite build')
    5. auditor -> (si falló y attempts < max) -> builder (bucle de auto-reparación focalizado)
               -> (si aprobó 0 errores) -> END (entrega verificada y lección persistida)
    """
    builder = StateGraph(FactorieState)

    builder.add_node("validate_task", validate_task)
    builder.add_node("spec_writer", spec_writer)
    builder.add_node("builder", builder_node)
    builder.add_node("auditor", auditor_node)

    # 1. Entrada a Validación
    builder.add_edge(START, "validate_task")

    # 2. Bifurcación tras validación
    builder.add_conditional_edges(
        "validate_task",
        route_after_task_validation,
        {
            "spec_writer": "spec_writer",
            END: END,
        },
    )

    # 3. Especificación -> Construcción
    builder.add_edge("spec_writer", "builder")

    # 4. Construcción -> Auditoría / Testing en tiempo real
    builder.add_edge("builder", "auditor")

    # 5. Bucle de Auto-Reparación (Self-Healing Loop) o Finalización
    builder.add_conditional_edges(
        "auditor",
        route_after_audit,
        {
            "builder": "builder",
            END: END,
        },
    )

    return builder.compile()


workflow = build_workflow()
