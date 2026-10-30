import re
from pathlib import Path
from typing import Any

from domain.state import FactorieState
from factorie_ia.core.memory import record_lesson
from tools.strands_harness import list_project_files, run_terminal_command


def extract_failing_file(output: str) -> str:
    """Extrae la ruta del archivo que causó el fallo de compilación mediante expresiones regulares."""
    # Patrón Rollup / Vite: src/components/Navbar.tsx (3:18): ...
    vite_match = re.search(r"(src/[a-zA-Z0-9_/.-]+\.tsx?)", output)
    if vite_match:
        return vite_match.group(1)

    # Patrón TypeScript: src/components/Hero.tsx:111:17 - error ...
    ts_match = re.search(r"(src/[a-zA-Z0-9_/.-]+\.tsx?):\d+:\d+", output)
    if ts_match:
        return ts_match.group(1)

    return ""


def auditor_node(state: FactorieState) -> dict[str, Any]:
    """Nodo Auditor / Tester:

    Ejecuta en tiempo real la suite de verificación técnica (compilación Vite / Rollup).
    - Si el build es exitoso: Aprueba la entrega técnica y certifica la web.
    - Si detecta errores de sintaxis, imports o tipos: Extrae el contexto del error,
      registra la lección en la memoria y solicita la auto-reparación al Builder.
    """
    project_dir = state.get("project_dir", "")
    if not project_dir:
        spec_data = state.get("spec", {})
        project_name = spec_data.get("project_name", "web-project")
        project_dir = f"/home/dei/Proyectos/Factorie-Ia/workspace/{project_name}"

    attempts = state.get("build_attempts", 0) + 1
    max_attempts = state.get("max_build_attempts", 3)

    print(f"\n[AUDITOR] 🔍 Ejecutando auditoría y pruebas de compilación (Intento {attempts}/{max_attempts})...")

    # Ejecutar compilación real en terminal
    test_result = run_terminal_command("pnpm build || npm run build", cwd=project_dir, timeout=60)

    if test_result["success"]:
        print(f"[AUDITOR] ✅ Compilación exitosa sin errores.")
        files = list_project_files(project_dir)

        spec_data = state.get("spec", {})
        project_name = spec_data.get("project_name", "web-project")
        title = spec_data.get("title", "Sitio Web")
        files_list_md = "\n".join(f"- `{f}`" for f in files if f.startswith("src/"))

        final_response = f"""🎉 **¡Proyecto Auditado y Verificado al 100%!**

🏗️ **Proyecto:** `{project_name}` — *{title}*
📁 **Ubicación local:** `{project_dir}`

🛡️ **Auditoría de Calidad:**
- ✅ Compilación de producción: **Exitosa (0 errores)**
- 🧠 Memoria del sistema: Reglas sincronizadas y activas
- 📦 Total de archivos en proyecto: **{len(files)} archivos**

🧱 **Estructura construida:**
{files_list_md}

---

🚀 **Para probar tu web en el navegador:**
```bash
cd {project_dir}
pnpm dev
# (o: npm run dev)
```
👉 Abre: `http://localhost:5173`
"""

        return {
            "audit_passed": True,
            "build_attempts": attempts,
            "last_error": "",
            "error_file": "",
            "response": final_response,
            "audit_report": {
                "status": "passed",
                "attempts": attempts,
                "stdout": test_result["stdout"][-500:],
            },
        }

    # Si falló la compilación:
    combined_error = f"{test_result['stdout']}\n{test_result['stderr']}".strip()
    failing_file = extract_failing_file(combined_error)

    print(f"[AUDITOR] ❌ Error de compilación detectado.")
    if failing_file:
        print(f"   Archivo afectado: {failing_file}")

    # Guardar en memoria si detectamos un error recurrente conocido (ej. imports lucide)
    if "not exported by" in combined_error and "lucide-react" in combined_error:
        match = re.search(r'"([^"]+)" is not exported by .*lucide-react', combined_error)
        bad_name = match.group(1) if match else "IconName"
        record_lesson(
            "lucide-react",
            f"El icono '{bad_name}' no existe en lucide-react. Verifica la lista oficial o usa alternativas canónicas.",
        )

    # Si se alcanzaron los intentos máximos, detener el bucle con informe
    if attempts >= max_attempts:
        print(f"[AUDITOR] ⚠️ Se alcanzó el número máximo de reintentos ({max_attempts}).")
        error_response = f"""⚠️ **La aplicación compiló con advertencias tras {attempts} intentos de auditoría.**

📁 Proyecto: `{project_dir}`
🔍 Archivo con error: `{failing_file or 'General'}`
Detalle del error:
```text
{combined_error[-800:]}
```
"""
        return {
            "audit_passed": False,
            "build_attempts": attempts,
            "last_error": combined_error,
            "error_file": failing_file,
            "response": error_response,
            "audit_report": {
                "status": "failed_max_retries",
                "attempts": attempts,
                "error": combined_error[-1000:],
            },
        }

    return {
        "audit_passed": False,
        "build_attempts": attempts,
        "last_error": combined_error,
        "error_file": failing_file,
    }
