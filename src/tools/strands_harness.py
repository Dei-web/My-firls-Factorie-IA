import os
import subprocess
from pathlib import Path
from typing import Any
from strands import tool

WORKSPACE_DIR = Path("/home/dei/Proyectos/Factorie-Ia/workspace")


@tool
def run_terminal_command(command: str, cwd: str | None = None, timeout: int = 120) -> dict[str, Any]:
    """Ejecuta un comando de terminal de forma segura dentro del espacio de trabajo del proyecto."""
    target_cwd = Path(cwd) if cwd else WORKSPACE_DIR
    target_cwd.mkdir(parents=True, exist_ok=True)

    try:
        process = subprocess.run(
            command,
            shell=True,
            cwd=str(target_cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": process.returncode == 0,
            "returncode": process.returncode,
            "stdout": process.stdout[-2000:] if process.stdout else "",
            "stderr": process.stderr[-2000:] if process.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Comando excedió el tiempo límite de {timeout}s",
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
        }


@tool
def write_project_file(project_dir: str, relative_path: str, content: str) -> dict[str, Any]:
    """Escribe un archivo de código dentro del proyecto asegurando la creación de directorios."""
    target_file = Path(project_dir) / relative_path
    try:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")
        return {
            "success": True,
            "path": str(target_file),
            "size_bytes": len(content.encode("utf-8")),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


@tool
def read_project_file(project_dir: str, relative_path: str) -> dict[str, Any]:
    """Lee el contenido de un archivo dentro del proyecto."""
    target_file = Path(project_dir) / relative_path
    if not target_file.exists():
        return {"success": False, "error": f"Archivo no encontrado: {relative_path}"}
    try:
        content = target_file.read_text(encoding="utf-8")
        return {"success": True, "content": content}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def list_project_files(project_dir: str) -> list[str]:
    """Lista todos los archivos creados en el proyecto excluyendo node_modules y .git."""
    base = Path(project_dir)
    if not base.exists():
        return []

    collected = []
    for root, dirs, files in os.walk(base):
        # Excluir carpetas pesadas
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", "dist", ".cache"}]
        for f in files:
            full = Path(root) / f
            collected.append(str(full.relative_to(base)))
    return sorted(collected)


def scaffold_react_template(project_name: str, title: str) -> Path:
    """Harness Scaffolding: Crea la estructura base de un proyecto React + Vite + Tailwind

    a partir de plantillas predefinidas (placeholders) para no desperdiciar tokens de LLM.
    """
    project_dir = WORKSPACE_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    package_json = f"""{{
  "name": "{project_name}",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "clsx": "^2.1.1",
    "framer-motion": "^12.4.7",
    "lucide-react": "^0.475.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "tailwind-merge": "^3.0.1"
  }},
  "devDependencies": {{
    "@types/node": "^22.13.4",
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.5.2",
    "tailwindcss": "^3.4.17",
    "typescript": "^5.7.3",
    "vite": "^6.1.0"
  }}
}}"""

    vite_config = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
"""

    tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""

    postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

    index_html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
  </head>
  <body class="bg-gray-50 text-gray-900 antialiased selection:bg-indigo-500 selection:text-white">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

    tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": false,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": false,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
"""

    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

html {
  scroll-behavior: smooth;
}
"""

    main_tsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""

    # Escribir archivos de configuración base
    write_project_file(str(project_dir), "package.json", package_json)
    write_project_file(str(project_dir), "vite.config.ts", vite_config)
    write_project_file(str(project_dir), "tailwind.config.js", tailwind_config)
    write_project_file(str(project_dir), "postcss.config.js", postcss_config)
    write_project_file(str(project_dir), "index.html", index_html)
    write_project_file(str(project_dir), "tsconfig.json", tsconfig)
    write_project_file(str(project_dir), "src/index.css", index_css)
    write_project_file(str(project_dir), "src/main.tsx", main_tsx)

    # Crear carpetas habituales
    (project_dir / "src" / "components").mkdir(parents=True, exist_ok=True)
    (project_dir / "src" / "data").mkdir(parents=True, exist_ok=True)

    return project_dir
