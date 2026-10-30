import json
from pathlib import Path
from typing import Any

from domain.spec import ProjectBuildArtifacts, RepairedFile
from domain.state import FactorieState
from factorie_ia.core.memory import format_memory_for_prompt, record_lesson
from factorie_ia.core.models_ia.nemotron import build_nemotron
from tools.strands_harness import (
    WORKSPACE_DIR,
    read_project_file,
    run_terminal_command,
    scaffold_react_template,
    write_project_file,
)


def _repair_failing_file(project_dir: str, file_path: str, error_msg: str) -> dict[str, Any]:
    """Sub-rutina de auto-reparación: toma el archivo que falló en compilación y lo corrige con el LLM."""
    print(f"\n[BUILDER / SELF-HEALING] 🩹 Reparando archivo '{file_path}' tras reporte del auditor...")

    file_data = read_project_file(project_dir, file_path)
    current_content = file_data.get("content", "")

    memory_context = format_memory_for_prompt()

    model = build_nemotron().with_structured_output(RepairedFile)

    prompt_system = f"""
Eres el Senior Fixer y Debugger de Factorie-Ia.
Un archivo de la aplicación web falló durante la compilación en terminal ('vite build').

{memory_context}

Tu objetivo es arreglar ÚNICAMENTE el archivo reportado para que compile sin errores.
Reglas:
1. Devuelve el código corregido completo en 'fixed_content', sin marcadores markdown.
2. En lucide-react, asegúrate de que todos los iconos importados existan exactamente en la librería (ej: Paintbrush en vez de PaintBrush, Pipette en vez de EyeDropper, Wrench en vez de Tool, Quote en vez de QuoteRight).
3. Corrige cualquier error de sintaxis, tipos o nombres no exportados.
4. Explica brevemente la solución y extrae una lección aprendida.
"""

    prompt_human = f"""
Archivo con error: {file_path}

Mensaje del compilador / Auditor:
```text
{error_msg}
```

Contenido actual del archivo:
```tsx
{current_content}
```

Corrige este archivo para que la aplicación compile al 100%.
"""

    repaired: RepairedFile = model.invoke(
        [
            ("system", prompt_system),
            ("human", prompt_human),
        ]
    )

    # Escribir la corrección en disco
    write_res = write_project_file(project_dir, file_path, repaired.fixed_content)
    if write_res["success"]:
        print(f"[BUILDER / SELF-HEALING] ✓ Archivo '{file_path}' actualizado en disco.")
        print(f"   Explicación: {repaired.explanation_of_fix}")
        if repaired.learned_rule:
            record_lesson("auto-healing", repaired.learned_rule)
    else:
        print(f"[BUILDER / SELF-HEALING] ✗ Fallo al escribir archivo reparado: {write_res.get('error')}")

    return {
        "builder_status": "repaired",
        "last_error": "",
    }


def builder_node(state: FactorieState) -> dict[str, Any]:
    """Nodo Builder: Da 'manos' al agente en la terminal usando el Strands Harness.

    Soporta dos modos:
    1. Modo Construcción Inicial: Scaffold base, instalación de dependencias y generación de componentes con memoria.
    2. Modo Auto-Reparación (Self-Healing Loop): Si el auditor reportó un error, corrige el archivo afectado.
    """
    spec_data = state.get("spec")
    if not spec_data:
        return {
            "builder_status": "error",
            "response": "⚠️ Error en Builder: No se encontró la especificación del proyecto.",
        }

    project_name = spec_data.get("project_name", "web-project")
    title = spec_data.get("title", "Sitio Web")
    project_dir = state.get("project_dir") or str(WORKSPACE_DIR / project_name)

    # 1. ¿Estamos en un ciclo de auto-reparación ordenado por el Auditor?
    last_error = state.get("last_error", "")
    error_file = state.get("error_file", "")
    if last_error and error_file:
        return _repair_failing_file(project_dir, error_file, last_error)

    # 2. Modo Construcción Inicial
    ui_theme = spec_data.get("ui_theme", "Moderno y responsivo con Tailwind CSS")
    components_info = json.dumps(spec_data.get("components", []), ensure_ascii=False)
    features_info = json.dumps(spec_data.get("key_features", []), ensure_ascii=False)

    print(f"\n[BUILDER] 1. Inicializando scaffolding para '{project_name}'...")
    dir_path = scaffold_react_template(project_name, title)
    project_dir = str(dir_path)

    # Paso 2: Asegurar dependencias si no existen en node_modules
    node_modules = Path(project_dir) / "node_modules"
    if not node_modules.exists():
        print(f"[BUILDER] 2. Instalando dependencias en {project_dir}...")
        install_res = run_terminal_command(
            "pnpm install || npm install",
            cwd=project_dir,
            timeout=90,
        )
        if not install_res["success"]:
            print(f"[BUILDER] Advertencia en instalación: {install_res['stderr'][:200]}")

    # Paso 3: Generación de componentes inyectando la Memoria Persistente
    print(f"[BUILDER] 3. Generando código de componentes para '{title}'...")
    memory_context = format_memory_for_prompt()

    model = build_nemotron().with_structured_output(ProjectBuildArtifacts)

    prompt_system = f"""
Eres el Lead Frontend Engineer y Builder Agent de Factorie-Ia.
Tienes "manos en la terminal" a través del Strands Harness para escribir archivos de código en disco.

{memory_context}

Tu misión es generar el código TypeScript / React de los componentes y la vista principal de la web.
El proyecto base ya cuenta con:
- React 18, Vite, TypeScript, Tailwind CSS, Lucide-React, Framer Motion y clsx.

REGLAS DE GENERACIÓN DE CÓDIGO:
1. Genera código limpio, moderno, completamente tipado y SIN sintaxis Markdown (sin ```tsx ni ```).
2. Los imports entre componentes locales deben omitir la extensión '.tsx' (ej: `import Hero from './components/Hero'`).
3. Diseña componentes visualmente atractivos, pulidos y responsivos utilizando clases de Tailwind CSS coherentes con la paleta estética solicitada.
4. Genera al menos:
   - `src/data/mockData.ts`: Archivo con datos realistas para poblar el sitio (textos, listas, servicios, obras, precios, etc.).
   - Los componentes solicitados en la lista de componentes (ej: `src/components/Navbar.tsx`, `src/components/Hero.tsx`, etc.).
   - `src/App.tsx`: La página principal que ensamble todos los componentes en un flujo visual completo, con interactividad básica.
5. Utiliza iconos de `lucide-react` cuando aporte valor visual.
6. En `lucide-react` utiliza únicamente nombres de iconos estándar verificados (ej: Paintbrush, Palette, Pipette, Wrench, Sparkles, Home, Star, Quote, Menu, X, Phone, Mail, Check, ArrowRight, ChevronRight, Clock, MapPin, Shield).
"""

    prompt_human = f"""
Especificación del Proyecto:
- Nombre: {project_name}
- Título: {title}
- Resumen: {spec_data.get('summary', '')}
- Estilo y Paleta Visual: {ui_theme}
- Componentes requeridos: {components_info}
- Funcionalidades clave: {features_info}

Genera los archivos de código necesarios para que la aplicación quede completamente funcional y lista para compilar.
"""

    artifacts: ProjectBuildArtifacts = model.invoke(
        [
            ("system", prompt_system),
            ("human", prompt_human),
        ]
    )

    # Paso 4: Escribir cada archivo generado en el disco usando el harness
    print(f"[BUILDER] 4. Escribiendo {len(artifacts.files)} archivos en disco...")
    for f in artifacts.files:
        write_res = write_project_file(project_dir, f.file_path, f.content)
        if write_res["success"]:
            print(f"   ✓ Creado: {f.file_path}")
        else:
            print(f"   ✗ Error al escribir {f.file_path}: {write_res.get('error')}")

    return {
        "builder_status": "built",
        "project_dir": project_dir,
        "code_artifacts": [f.model_dump() for f in artifacts.files],
        "build_attempts": 0,
        "max_build_attempts": 3,
        "last_error": "",
        "error_file": "",
    }
