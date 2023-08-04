from pydantic import Field


class CreateTodoList:
    name: str = Field(max_length=100)
    description: str
