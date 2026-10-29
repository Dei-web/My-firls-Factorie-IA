from typing import Protocol

from domain.state import TaskRequest, TaskResult


class TaskInputPort(Protocol):
    def submit(self, request: TaskRequest) -> TaskResult: ...
