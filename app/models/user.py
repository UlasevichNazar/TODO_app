import uuid
from enum import Enum

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import AbstractBaseModel
from app.models.task import Task  # noqa: F401
from app.models.todo_list import ToDoList  # noqa: F401


class Roles(str, Enum):
    ROLE_USER = "USER"
    ROLE_ADMIN = "ADMIN"


class User(AbstractBaseModel):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column("Username", String(length=60), unique=True, nullable=False)
    email = Column("Email", String, unique=True, nullable=False)
    password = Column("Password", String, nullable=False)
    is_active = Column("Is_active", Boolean, default=True)
    roles = Column("User role", ARRAY(String), nullable=False, default=Roles.ROLE_USER)
    todo_lists = relationship("ToDoList", back_populates="user")
