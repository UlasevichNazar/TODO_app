from datetime import datetime
from uuid import UUID

from pydantic import Field
from pydantic import field_validator

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
    created_at: datetime
    updated_at: datetime


class ShowTodoListSchema(TunedModel):
    id: UUID
    name: str = Field(max_length=100)
    description: str
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    def validate_created_at(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%d-%m-%Y %H:%M")
