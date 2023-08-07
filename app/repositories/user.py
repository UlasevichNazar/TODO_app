from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_all_users(self) -> List[User]:
        stmt = select(User)
        return await self.get_all(stmt)

    async def get_user_by_id(self, user_id: UUID) -> Optional[UUID]:
        query = select(User).where(User.id == user_id)
        return await self.get_by_id(query)

    async def create_user(self, username: str, email: str, password: str) -> User:
        new_user = User(username=username, email=email, password=password)
        return await self.create(new_user)

    async def updated_user(self, user_id: UUID, **kwargs) -> Optional[UUID]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.id)
        )
        return await self.update(query)

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        query = (
            delete(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .returning(User.id)
        )
        return await self.delete(query)
