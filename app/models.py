from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import TIMESTAMP

from database.database import Base


class AbstractBaseModel(Base):
    __abstract__ = True

    created_at = Column("Created at", TIMESTAMP, default=datetime.utcnow)
    updated_at = Column("Updated at", TIMESTAMP, default=datetime.utcnow)
