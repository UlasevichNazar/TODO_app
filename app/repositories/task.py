from typing import Optional
from typing import Tuple
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.base import BaseRepository
from app.schemas.task import CreateTaskSchema


class TaskRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_new_task(self, values: CreateTaskSchema) -> Task:
        new_task = Task(**values.model_dump())
        return await self._create(new_task)

    async def get_tasks(self, todo_list_ids: Tuple[UUID]):
        query = select(Task).filter(Task.todo_list_id.in_(todo_list_ids))
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_user_task(
        self, task_id: UUID, todo_list_ids: Tuple[UUID]
    ) -> Optional[Task]:
        query = select(Task).filter(
            and_(Task.id == task_id, Task.todo_list_id.in_(todo_list_ids))
        )
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def updating_task_by_user(self, instance: Task, **kwargs) -> Result[Task]:
        return await self._update(Task, instance, kwargs)

    async def deleting_task_by_user(self, task: Task) -> None:
        return await self._delete(task)
