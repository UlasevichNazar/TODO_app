import uuid
from typing import List
from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from app.enums import Roles
from app.models.base import AbstractBaseModel

if TYPE_CHECKING:
    from app.models.todo_list import ToDoList


class User(AbstractBaseModel):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        "Username", String(length=60), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column("Email", String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column("Password", String, nullable=False)
    is_active: Mapped[bool] = mapped_column("Is_active", Boolean, default=True)
    roles: Mapped[str] = mapped_column(
        "User role", Enum(Roles), nullable=False, default=Roles.ROLE_USER
    )
    todo_lists: Mapped[List["ToDoList"]] = relationship(
        "ToDoList", back_populates="user"
    )
