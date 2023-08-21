from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from sqlalchemy import Result

from app.models.user import Roles
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema
from app.utils.password_hasher import PasswordService
from database.database import async_session


class UserService:
    @staticmethod
    async def get_user(user_id: UUID) -> Optional[User]:
        async with async_session() as session:
            getting_user = UserRepository(session)
            user = await getting_user.get_user_by_id(user_id)
            if user is not None:
                return user

    @staticmethod
    async def get_all_users(user: User) -> Union[List[User], Optional[User]]:
        async with async_session() as session:
            user_repo = UserRepository(session)
            if Roles.ROLE_ADMIN in user.roles:
                users = await user_repo.get_all_users()
            else:
                users = await user_repo.get_user_by_id(user.id)
            return users

    @staticmethod
    async def get_user_by_username_for_auth(username: str):
        async with async_session() as session:
            user = UserRepository(session)
            return await user.get_user_by_username(username=username)

    @staticmethod
    async def create_new_user(body: CreateUserSchema) -> User:
        async with async_session() as session:
            user = await UserService._create_user(values=body)
            creation_user = await UserRepository(session).create_user(user)
            await session.commit()
            return creation_user

    @staticmethod
    async def _create_user(values: CreateUserSchema) -> User:
        values_for_create = values.model_dump()
        values_for_create["password"] = PasswordService.get_password_hash(
            values.password
        )
        new_user = User(**values_for_create)
        return new_user

    @staticmethod
    async def create_admin(body: CreateUserSchema) -> User:
        async with async_session() as session:
            user = await UserService._create_admin_user(values=body)
            creation_user = await UserRepository(session).create_user(user)
            await session.commit()
            return creation_user

    @staticmethod
    async def _create_admin_user(values: CreateUserSchema) -> User:
        values_for_create = values.model_dump()
        values_for_create["roles"] = Roles.ROLE_ADMIN
        values_for_create["password"] = PasswordService.get_password_hash(
            values.password
        )
        new_user = User(**values_for_create)
        return new_user

    @staticmethod
    async def update_user(updated_params: dict, user_id: UUID) -> Result[User]:
        async with async_session() as session:
            updating_user = UserRepository(session)
            user = await updating_user.get_user_by_id(user_id=user_id)
            updated_user = await updating_user.updated_user(user, **updated_params)
            await session.commit()
            return updated_user

    @staticmethod
    async def deleting_user(user: User) -> None:
        async with async_session() as session:
            deleting_user = UserRepository(session)
            deleting_user_obj = await deleting_user.delete_user(user=user)
            await session.commit()
            return deleting_user_obj
