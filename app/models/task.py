import enum
import uuid

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import AbstractBaseModel


class TaskStatus(enum.Enum):
    IN_PROGRESS = "In progress"
    DONE = "Done"


class Task(AbstractBaseModel):
    __tablename__ = "tasks"

    id = Column("Task id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("Name", String(length=100), nullable=False)
    description = Column("Description", Text, default="")
    status = Column(Enum(TaskStatus), default=TaskStatus.IN_PROGRESS)
    todo_list_id = Column(
        UUID(as_uuid=True), ForeignKey("todo_lists.id"), nullable=False
    )
    todo_list = relationship("ToDoList", back_populates="tasks")
