from domain.spec import WebSpecification
from domain.state import FactorieState
from factorie_ia.core.models_ia.nemotron import build_nemotron


def format_spec_as_markdown(spec: WebSpecification) -> str:
    """Convierte la especificación técnica estructurada en un reporte legible en Markdown."""
    components_str = "\n".join(
        f"- **`{c.name}`**: {c.purpose}" for c in spec.components
    )
    features_str = "\n".join(f"- {feat}" for feat in spec.key_features)
    builder_inst_str = "\n".join(
        f"{idx + 1}. {inst}" for idx, inst in enumerate(spec.builder_instructions)
    )
    stack_str = ", ".join(spec.tech_stack)

    return f"""📋 **Especificación Técnica del Proyecto: {spec.title}**
*Identificador:* `{spec.project_name}`

### 🎯 Resumen del Proyecto
{spec.summary}

- **Público Objetivo:** {spec.target_audience}
- **Stack Tecnológico:** {stack_str}
- **Estilo y Paleta Visual:** {spec.ui_theme}

---

### 💻 Comando de Scaffolding (Terminal Harness)
```bash
{spec.scaffold_command}
```

---

### 🧩 Componentes a Desarrollar
{components_str}

---

### ⚡ Funcionalidades Clave
{features_str}

---

### 🛠️ Instrucciones para el Builder Agent
{builder_inst_str}
"""


def spec_writer(state: FactorieState) -> dict:
    """Nodo Spec Writer: Enriquece la solicitud del usuario generando una especificación

    técnica exhaustiva para el Builder Agent y los subagentes.
    """
    model = build_nemotron().with_structured_output(WebSpecification)

    user_task = state["task"]
    task_category = state.get("task_category", "web general")

    result: WebSpecification = model.invoke(
        [
            (
                "system",
                """
Eres el Senior Spec Writer y Arquitecto de Producto de Factorie-Ia.

Tu función es transformar una solicitud inicial del usuario (que puede ser corta o vaga,
como por ejemplo 'generame un web de pintura') en una ESPECIFICACIÓN TÉCNICA DETALLADA,
completa y lista para ser ejecutada por el agente constructor (Builder Agent).

El Builder Agent tendrá acceso a terminal ("manos en la terminal" mediante un harness
como strandsagents.com) para crear el proyecto e instalar dependencias.

Debes definir con precisión:
1. project_name: nombre del proyecto en formato kebab-case (ej: 'estudio-pintura-art').
2. title: título comercial del sitio.
3. summary: descripción ampliada del negocio, tono de la marca y contenido.
4. target_audience: quiénes visitarán la página y qué valor buscan.
5. tech_stack: stack moderno recomendado (ej: React, Vite, TailwindCSS, Lucide-React).
6. scaffold_command: comando de inicialización de terminal (ej: 'npm create vite@latest {{project_name}} -- --template react-ts').
7. ui_theme: guía estética (paleta de colores sugerida, tipografía, estilo visual limpio y responsivo).
8. components: lista de componentes modulares con su propósito específico.
9. key_features: funcionalidades clave e interactivas de la web.
10. builder_instructions: pasos técnicos ordenados para el Builder Agent (scaffold, setup Tailwind, crear componentes, armar vista principal).

Enfócate en generar una especificación práctica, realista y de alta calidad para React/Vite.
""",
            ),
            (
                "human",
                f"Categoría: {task_category}\nSolicitud del usuario: {user_task}",
            ),
        ]
    )

    spec_markdown = format_spec_as_markdown(result)

    return {
        "spec": result.model_dump(),
        "spec_markdown": spec_markdown,
        "response": spec_markdown,
    }
