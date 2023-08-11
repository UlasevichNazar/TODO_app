from uuid import UUID

from pydantic import Field

from app.schemas.base import TunedModel
from app.schemas.user import ShowUserSchema


class CreateTodoListSchema(TunedModel):
    name: str = Field(max_length=100)
    description: str = ""
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "todo_list",
                "description": "your description",
            }
        }
    }


class ShowTodoListForCreateSchema(TunedModel):
    id: UUID
    name: str = Field(max_length=100)
    description: str
    user: ShowUserSchema


class ShowTodoListSchema(TunedModel):
    id: UUID
    name: str = Field(max_length=100)
    description: str
