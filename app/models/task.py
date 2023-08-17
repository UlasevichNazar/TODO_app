import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.enums import TaskStatus
from app.models.base import AbstractBaseModel

if TYPE_CHECKING:
    from app.models.todo_list import ToDoList


class Task(AbstractBaseModel):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        "Task id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column("Name", String(length=100), nullable=False)
    description: Mapped[str] = mapped_column("Description", Text, default="")
    status: Mapped[str] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.IN_PROGRESS
    )
    todo_list_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("todo_lists.id"), nullable=False
    )
    todo_list: Mapped["ToDoList"] = relationship("ToDoList", back_populates="tasks")
