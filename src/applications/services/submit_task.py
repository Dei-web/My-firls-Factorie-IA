from applications.ports.task_input import TaskInputPort
from domain.state import TaskRequest, TaskResult
from factorie_ia.core.workflow import workflow


class SubmitTask(TaskInputPort):
    def submit(self, request: TaskRequest) -> TaskResult:
        result = workflow.invoke(
            {
                "task": request.description,
                "source": request.source,
                "response": "",
            }
        )
        # print("RESULTADO LANGGRAPH:", repr(result))
        response = result.get("response") or "No se pudo generar una respuesta."
        return TaskResult(response=response)
