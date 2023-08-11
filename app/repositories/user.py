from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_all_users(self) -> List[User]:
        return await self.get_all(User)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.get_by_id(User, user_id)

    async def create_user(
        self, username: str, email: str, password: str, roles: list
    ) -> User:
        new_user = User(username=username, email=email, password=password, roles=roles)
        return await self.create(new_user)

    async def updated_user(self, instance: User, values: dict):
        return await self.update(User, instance, values)

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        return await self.delete(User, user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]
