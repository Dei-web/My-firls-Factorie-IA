from domain.state import FactorieState
from langgraph.graph import END


def route_after_task_validation(state: FactorieState) -> str:
    """Enruta hacia spec_writer si la tarea es válida para desarrollo web,

    o hacia END si no fue aprobada por el validador inicial.
    """
    if state.get("task_valid"):
        return "spec_writer"

    return END


def route_after_audit(state: FactorieState) -> str:
    """Bucle de retroalimentación en tiempo real:

    - Si la auditoría pasa (0 errores de compilación): Concluye exitosamente (o pasa a subagentes).
    - Si la auditoría detecta errores y aún quedan intentos: Regresa al 'builder' para auto-reparación.
    - Si se superó el límite de reintentos: Termina en END con informe del error.
    """
    if state.get("audit_passed"):
        print("[ROUTER] 🟢 Auditoría aprobada al 100%. Avanzando a finalización.")
        return END

    attempts = state.get("build_attempts", 0)
    max_attempts = state.get("max_build_attempts", 3)
    error_file = state.get("error_file", "")

    if attempts < max_attempts and error_file:
        print(f"[ROUTER] 🔁 Bucle de auto-reparación activado ({attempts}/{max_attempts}). Reenviando a Builder...")
        return "builder"

    print("[ROUTER] 🔴 Límite de reintentos alcanzado o sin archivo identificado. Finalizando.")
    return END
