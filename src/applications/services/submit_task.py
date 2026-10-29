from applications.ports.task_input import TaskInputPort
from factorie_ia.core.workflow import workflow
from domain.state import TaskRequest, TaskResult


class SubmitTask:
    def submit(self, request: TaskRequest) -> TaskResult:
        result = workflow.invoke(
            {
                "task": request.description,
                "response": "",
            }
        )

        return TaskResult(response=result["response"])
