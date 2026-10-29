from typing import TypedDict
from pydantic import BaseModel, Field


class FactorieState(TypedDict):
    task: str
    response: str


class TaskRequest(BaseModel):
    description: str = Field(min_length=1)
    source: str = "unknown"


class TaskResult(BaseModel):
    response: str
