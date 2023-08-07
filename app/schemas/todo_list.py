import typing
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from app.schemas.task import CreateTaskSchema


class CreateTodoListSchema(BaseModel):
    name: str = Field(max_length=100)
    description: Optional[str] = None
    tasks: Optional[typing.List[CreateTaskSchema]] = None
