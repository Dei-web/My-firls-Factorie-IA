from applications.services.submit_task import SubmitTask
from domain.state import TaskRequest


def run_cli() -> None:
    service = SubmitTask()

    request = TaskRequest(
        description="Crear una página web",
        source="cli",
    )

    result = service.submit(request)

    print(result.response)
