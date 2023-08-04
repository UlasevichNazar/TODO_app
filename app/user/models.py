import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models import AbstractBaseModel


class User(AbstractBaseModel):
    __tablename__ = "users"
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column("Username", String(length=60), unique=True, nullable=False)
    email = Column("Email", String, unique=True, nullable=False)
    password = Column("Password", String, nullable=False)
    is_active = Column("Is_active", Boolean, default=True)
    todo_list = relationship("ToDoList", back_populates="users")
