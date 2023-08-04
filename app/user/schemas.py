import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator

LETTER_MATCH_PATTERN = re.compile(r"^[a-zA-Zа-яА-Я\-]+$")


class CreateUser(BaseModel):
    username: str = Field(max_length=60, min_length=1)
    email: EmailStr
    password: str
    model_config = {
        "json_schema_extra": {
            "example": [
                {
                    "username": "user",
                    "email": "user@useremail.com",
                    "password": "userpassword",
                }
            ]
        }
    }

    @field_validator("username")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Username should contains only letters"
            )
        return value


class ShowUser(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
