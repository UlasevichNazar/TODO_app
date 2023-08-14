from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import select

from app.models.todo_list import ToDoList
from app.models.user import User
from app.repositories.base import BaseRepository


class TodoListRepository(BaseRepository):
    async def create_todo(self, name: str, description: str, user_id: UUID) -> User:
        new_list = ToDoList(name=name, description=description, user_id=user_id)
        return await self.create(new_list)

    async def get_all_user_lists(self, user_id: UUID) -> List[ToDoList]:
        query = select(ToDoList).filter_by(user_id=user_id)
        res = await self.db_session.execute(query)
        return res.scalars().all()

    async def get_list_by_id(self, list_id: UUID) -> Optional[ToDoList]:
        return await self.get_by_id(ToDoList, list_id)

    async def update_list_by_user(self, instance: ToDoList, values: dict):
        return await self.update(ToDoList, instance, values)

    async def deleting_todo(self, list_id: UUID) -> Optional[UUID]:
        return await self.delete(ToDoList, list_id)
