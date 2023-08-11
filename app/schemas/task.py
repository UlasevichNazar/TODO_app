from typing import Optional

from pydantic import Field

from app.models.task import TaskStatus
from app.schemas.base import TunedModel


class CreateTaskSchema(TunedModel):
    name: str = Field(max_length=100)
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.IN_PROGRESS
    todo_list_id: int
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "create something",
                "description": "we should to create somethings",
                "status": "In progress",
                "todo_list_id": 1,
            }
        }
    }


class ShowTaskSchema(TunedModel):
    name: str
    description: str
    status: TaskStatus
    todo_list_id: int
