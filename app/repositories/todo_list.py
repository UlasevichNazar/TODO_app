from typing import Optional
from uuid import UUID

from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo_list import ToDoList
from app.repositories.base import BaseRepository


class TodoListRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_todo(self, new_list: ToDoList) -> ToDoList:
        return await self._create(new_list)

    async def get_all_user_lists(self, user_id: UUID):
        query = select(ToDoList).filter_by(user_id=user_id)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_list_by_id(self, list_id: UUID) -> Optional[ToDoList]:
        return await self._get(ToDoList, list_id)

    async def update_list_by_user(
        self, instance: ToDoList, **kwargs
    ) -> Result[ToDoList]:
        return await self._update(ToDoList, instance, kwargs)

    async def deleting_todo(self, todo_list: ToDoList) -> None:
        return await self._delete(todo_list)
