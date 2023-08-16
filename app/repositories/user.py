from typing import List
from typing import Optional
from uuid import UUID

from sqlalchemy import Result
from sqlalchemy import select

from app.models.user import Roles
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import CreateUserSchema
from app.services.hashing import Hasher


class UserRepository(BaseRepository):
    async def get_all_users(self) -> List[User]:
        return await self.get_all(User)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.get_by_id(User, user_id)

    async def create_user(self, values: CreateUserSchema) -> User:
        values_for_create = values.model_dump()
        values_for_create["password"] = Hasher.get_password_hash(values.password)
        new_user = User(**values_for_create)
        return await self.create(new_user)

    async def create_admin_user(self, values: CreateUserSchema) -> User:
        values_for_create = values.model_dump()
        values_for_create["roles"] = [Roles.ROLE_ADMIN]
        values_for_create["password"] = Hasher.get_password_hash(values.password)
        new_user = User(**values_for_create)
        return await self.create(new_user)

    async def updated_user(self, instance: User, **kwargs) -> Result[User]:
        return await self.update(User, instance, kwargs)

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        return await self.delete(User, user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        res = await self.db_session.execute(query)
        user = res.fetchone()
        if user is not None:
            return user[0]
