import sys

from applications.services.submit_task import SubmitTask
from domain.state import TaskRequest


def run_cli() -> None:
    service = SubmitTask()

    task_desc = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "generame un web de pintura"

    request = TaskRequest(
        description=task_desc,
        source="cli",
    )

    result = service.submit(request)

    print(result.response)
