import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import AbstractBaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task import Task


class ToDoList(AbstractBaseModel):
    __tablename__ = "todo_lists"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column("Name", String(length=101), nullable=False)
    description: Mapped[str] = mapped_column("Description", Text, default="")
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="todo_lists")
    tasks: Mapped["Task"] = relationship(
        "Task", back_populates="todo_list", cascade="all, delete-orphan"
    )
