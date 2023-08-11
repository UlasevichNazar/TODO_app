import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import AbstractBaseModel
from app.models.task import Task  # noqa: F401


class ToDoList(AbstractBaseModel):
    __tablename__ = "todo_lists"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("Name", String(length=100), nullable=False)
    description = Column("Description", Text, default="")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="todo_lists")
    tasks = relationship("Task", back_populates="todo_list")
