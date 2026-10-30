from pydantic import BaseModel, Field


class TaskValidation(BaseModel):
    is_valid_task: bool = Field(
        description="True si la solicitud es una petición comprensible para crear o modificar una web o proyecto de software. False si es un saludo, texto aleatorio o una consulta ajena al desarrollo web."
    )
    task_category: str = Field(
        description="Categoría de la tarea (ej: 'landing_page', 'portfolio', 'ecommerce', 'web_app', 'dashboard', 'otro')."
    )
    reason: str = Field(
        description="Explicación clara de por qué es válida o qué falta si no es válida para orientar al usuario."
    )


class ComponentSpec(BaseModel):
    name: str = Field(
        description="Nombre del componente en PascalCase (ej: HeroSection, ArtGallery, ContactModal)."
    )
    purpose: str = Field(
        description="Propósito, contenido clave e interacción esperada del componente."
    )


class WebSpecification(BaseModel):
    project_name: str = Field(
        description="Identificador del proyecto en kebab-case (ej: 'galeria-pintura-art')."
    )
    title: str = Field(
        description="Título profesional del sitio web."
    )
    summary: str = Field(
        description="Descripción ampliada y detallada del negocio o temática de la página."
    )
    target_audience: str = Field(
        description="Público objetivo y propuesta de valor de la página."
    )
    tech_stack: list[str] = Field(
        description="Stack tecnológico base recomendado (ej: ['React', 'Vite', 'TailwindCSS', 'Lucide-React'])."
    )
    scaffold_command: str = Field(
        description="Comando de terminal placeholder para inicializar el proyecto (ej: 'npm create vite@latest {{project_name}} -- --template react-ts')."
    )
    ui_theme: str = Field(
        description="Especificación estética: paleta de colores sugerida, estilo visual y tipografía."
    )
    components: list[ComponentSpec] = Field(
        description="Lista de componentes esenciales a desarrollar."
    )
    key_features: list[str] = Field(
        description="Funcionalidades interactivas clave (ej: catálogo interactivo, formulario de contacto, filtros)."
    )
    builder_instructions: list[str] = Field(
        description="Instrucciones directas, técnicas y secuenciales para el Builder Agent."
    )


class GeneratedFile(BaseModel):
    file_path: str = Field(
        description="Ruta relativa del archivo (ej: 'src/components/Hero.tsx', 'src/data/mockData.ts', 'src/App.tsx')."
    )
    content: str = Field(
        description="Código fuente TypeScript / React completo y ejecutable, sin bloques markdown ni explicaciones adicionales."
    )
    purpose: str = Field(
        description="Propósito y elementos implementados en este archivo."
    )


class ProjectBuildArtifacts(BaseModel):
    files: list[GeneratedFile] = Field(
        description="Lista de archivos React y TypeScript necesarios para completar la aplicación."
    )
    summary_of_work: str = Field(
        description="Resumen de los componentes desarrollados y la arquitectura de la interfaz."
    )


class RepairedFile(BaseModel):
    file_path: str = Field(
        description="Ruta relativa del archivo que fue reparado."
    )
    fixed_content: str = Field(
        description="Código fuente completo ya corregido y listo para compilar sin bloques markdown."
    )
    explanation_of_fix: str = Field(
        description="Explicación técnica de la corrección realizada."
    )
    learned_rule: str = Field(
        description="Regla o lección aprendida concisa para guardar en la memoria persistente del sistema."
    )
