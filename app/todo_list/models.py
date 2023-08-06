import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models import AbstractBaseModel


class ToDoList(AbstractBaseModel):
    __tablename__ = "todo_lists"
    list_id = Column(
        "ToDo list id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name = Column("Name", String(length=100), nullable=False)
    description = Column("Description", Text, default="")
    user_id = Column(UUID, ForeignKey("users.id"))
    user = relationship("User", back_populates="todo_lists")
    tasks = relationship("Task", back_populates="todo_lists")
