from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class AbstractBaseModel(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[TIMESTAMP] = mapped_column(
        "Created at", TIMESTAMP, default=datetime.utcnow
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        "Updated at", TIMESTAMP, default=datetime.utcnow
    )
