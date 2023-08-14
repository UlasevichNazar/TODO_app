from typing import Optional
from uuid import UUID

from pydantic import Field

from app.models.task import TaskStatus
from app.schemas.base import TunedModel


class CreateTaskSchema(TunedModel):
    name: str = Field(max_length=100)
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.IN_PROGRESS
    todo_list_id: UUID
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "create something",
                "description": "we should to create somethings",
                "todo_list_id": "gf448879-cfe8-56e9-a2c2-11ac4e79e37d",
            }
        }
    }


class ShowTaskSchema(TunedModel):
    id: UUID
    name: str
    description: str
    status: TaskStatus
    todo_list_id: UUID
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "df448879-cfe8-46e9-a2v2-13ac4679e47d",
                "name": "create something",
                "description": "we should to create somethings",
                "status": "In progress",
                "todo_list_id": "gf448879-cfe8-56e9-a2c2-11ac4e79e37d",
            }
        }
    }
