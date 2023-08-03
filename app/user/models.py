from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.models import AbstractBaseModel


class User(AbstractBaseModel):
    __tablename__ = "users"
    id = Column("Id", Integer, primary_key=True, index=True)
    username = Column("Username", String, unique=True, nullable=False)
    email = Column("Email", String, unique=True, nullable=False)
    password = Column("Password", String, nullable=False)
    is_active = Column("Is_active", Boolean, default=True)
