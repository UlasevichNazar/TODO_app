from sqlalchemy import func
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class AbstractBaseModel(Base):
    __abstract__ = True

    created_at: Mapped[TIMESTAMP] = mapped_column(
        "Created at", TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        "Updated at",
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
