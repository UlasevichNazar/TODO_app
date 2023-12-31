import re
import uuid
from typing import Optional

from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator

from app.exceptions.exceptions import EmptyParametersException
from app.schemas.base import TunedModel

LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Zа-яА-Я\-]+$")


class CreateUserSchema(TunedModel):
    username: str = Field(max_length=60, min_length=1)
    email: EmailStr
    password: str = Field(min_length=8, max_length=24, description="user password")
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "user",
                "email": "user@useremail.com",
                "password": "userpassword",
            }
        }
    }

    @classmethod
    @field_validator("username")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise EmptyParametersException(
                detail="Username should contains only letters"
            )
        return value


class ShowUserSchema(TunedModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "fdbb8ed7-c839-4a21-b8a2-35c023371143",
                "username": "user",
                "email": "user@user_email.com",
                "is_active": "true",
            }
        }
    }


class ShowAdminSchema(TunedModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    roles: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "fdbb8ed7-c839-4a21-b8a2-35c023371143",
                "username": "admin-user",
                "email": "admin@admin_email.com",
                "is_active": "true",
                "roles": ["Admin"],
            }
        }
    }


class UpdateUserRequestSchema(TunedModel):
    username: Optional[str] = Field(default=None, max_length=60, description="username")
    email: Optional[EmailStr] = Field(default=None, description="user email")
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "updating_user_username",
                "email": "updating_email@user_email.com",
            }
        }
    }

    @classmethod
    @field_validator("username")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise EmptyParametersException(
                detail="Username should contains only letters"
            )
        return value
