from typing import List
from typing import Optional
from typing import Tuple
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import select

from app.models.task import Task
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository):
    async def create_new_task(
        self, name: str, description: str, todo_list_id: UUID
    ) -> Task:
        new_task = Task(name=name, description=description, todo_list_id=todo_list_id)
        return await self.create(new_task)

    async def get_tasks(self, todo_list_ids: Tuple[UUID]) -> List[Task]:
        query = select(Task).filter(Task.todo_list_id.in_(todo_list_ids))
        res = await self.db_session.execute(query)
        return res.scalars().all()

    async def get_user_task(
        self, task_id: UUID, todo_list_ids: Tuple[UUID]
    ) -> Optional[Task]:
        query = select(Task).filter(
            and_(Task.id == task_id, Task.todo_list_id.in_(todo_list_ids))
        )
        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()
