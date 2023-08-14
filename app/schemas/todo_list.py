import uuid
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
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "df448879-cfe8-46e9-a2v2-13ac4679e47d",
                "name": "todo_list",
                "description": "your description",
                "user": {
                    "id": "3fa85fb4-5717-4g12-b3fc-2c923f56afa6",
                    "username": "user",
                    "email": "user@example.com",
                    "is_active": "true",
                },
                "created_at": "01-01-2000 00:00",
                "updated_at": "01-01-2000 00:00",
            }
        }
    }


class ShowTodoListSchema(TunedModel):
    id: UUID
    name: str = Field(max_length=100)
    description: str
    created_at: datetime
    updated_at: datetime
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "df448879-cfe8-46e9-a2v2-13ac4679e47d",
                "name": "todo_list",
                "description": "your description",
                "created_at": "01-01-2000 00:00",
                "updated_at": "01-01-2000 00:00",
            }
        }
    }

    @field_validator("created_at", "updated_at")
    def validate_created_at(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%d-%m-%Y %H:%M")


class UpdateTodoListSchema(TunedModel):
    name: str = Field(max_length=100)
    description: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "todo_list",
                "description": "your description",
            }
        }
    }


class DeleteTodoListSchema(TunedModel):
    deleted_todo_list_id: uuid.UUID
    model_config = {
        "json_schema_extra": {
            "example": {
                "deleted_todo_list_id": "df448879-cfe8-46e9-a2v2-13ac4679e47d",
            }
        }
    }
