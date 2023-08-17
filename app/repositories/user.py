from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_all_users(self) -> List[User]:
        return await self._get_all(User)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self._get(User, user_id)

    async def create_user(self, user: User) -> User:
        return await self._create(user)

    async def updated_user(self, instance: User, **kwargs) -> Result[User]:
        return await self._update(User, instance, kwargs)

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        return await self._delete(User, user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username).fetch(count=1)
        res = await self.session.execute(query)
        return res.scalar()
