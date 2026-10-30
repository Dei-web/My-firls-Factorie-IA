import json
from pathlib import Path
from typing import Any

MEMORY_FILE = Path("/home/dei/Proyectos/Factorie-Ia/workspace/.memory/lessons_learned.json")


def load_persistent_memory() -> list[dict[str, Any]]:
    """Carga las reglas, lecciones y aprendizajes previos persistidos en disco."""
    if not MEMORY_FILE.exists():
        # Memoria base inicial por defecto
        initial_lessons = [
            {
                "topic": "lucide-react",
                "lesson": "Usa nombres oficiales canónicos en minúsculas después del prefijo: 'Paintbrush' (no PaintBrush), 'Pipette' (no EyeDropper), 'Wrench' (no Tool), 'Quote' (no QuoteRight).",
            },
            {
                "topic": "imports",
                "lesson": "En imports locales de TypeScript con Vite nunca agregues la extensión '.tsx' (ej: 'import Hero from ./components/Hero').",
            },
            {
                "topic": "events",
                "lesson": "En eventos táctiles o de ratón de React, usa tipos sintéticos de React (React.TouchEvent o React.MouseEvent) en lugar de TouchEvent nativo.",
            },
        ]
        save_persistent_memory(initial_lessons)
        return initial_lessons

    try:
        data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_persistent_memory(lessons: list[dict[str, Any]]) -> None:
    """Guarda las lecciones aprendidas en disco."""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(lessons, indent=2, ensure_ascii=False), encoding="utf-8")


def record_lesson(topic: str, lesson: str) -> None:
    """Registra un nuevo aprendizaje extraído de una corrección o error en tiempo de compilación."""
    lessons = load_persistent_memory()
    # Evitar duplicados exactos
    if any(item.get("lesson") == lesson for item in lessons):
        return

    lessons.append({"topic": topic, "lesson": lesson})
    save_persistent_memory(lessons)


def format_memory_for_prompt() -> str:
    """Devuelve un resumen formateado de las lecciones aprendidas para inyectar en el contexto del LLM."""
    lessons = load_persistent_memory()
    if not lessons:
        return ""

    lines = ["🧠 **Reglas aprendidas de compilaciones y auditorías previas:**"]
    for idx, item in enumerate(lessons):
        lines.append(f"- [{item.get('topic', 'General')}]: {item.get('lesson')}")
    return "\n".join(lines)
