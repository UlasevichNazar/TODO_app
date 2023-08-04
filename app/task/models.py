import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship  # noqa: F401
from sqlalchemy_utils.types.choice import ChoiceType

from app.models import AbstractBaseModel


class Task(AbstractBaseModel):
    IN_PROGRESS = "In progress"
    DONE = "Done"

    STATUSES = [("in_progress", IN_PROGRESS), ("done", DONE)]
    task_id = Column(
        "Task id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name = Column("Name", String(length=100), nullable=False)
    description = Column("Description", Text, default="")
    status = Column(ChoiceType(STATUSES), default=IN_PROGRESS)
