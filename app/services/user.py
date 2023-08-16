from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from sqlalchemy import Result

from app.models.user import Roles
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema
from app.schemas.user import ShowAdminSchema
from app.schemas.user import ShowUserSchema
from database.database import async_session


async def get_user(user_id: UUID) -> Optional[User]:
    async with async_session() as session:
        async with session.begin():
            getting_user = UserRepository(session)
            user = await getting_user.get_user_by_id(user_id)
            if user is not None:
                return user


async def get_all_users(user: User) -> Union[List[User], Optional[User]]:
    async with async_session() as session:
        async with session.begin():
            user_repo = UserRepository(session)
            if Roles.ROLE_ADMIN in user.roles:
                users = await user_repo.get_all_users()
            else:
                users = await user_repo.get_user_by_id(user.id)
            return users


async def get_user_by_username_for_auth(username: str):
    async with async_session() as session:
        async with session.begin():
            user = UserRepository(session)
            return await user.get_user_by_username(username=username)


async def create_new_user(body: CreateUserSchema) -> ShowUserSchema:
    async with async_session() as session:
        async with session.begin():
            new_user = UserRepository(session)
            user = await new_user.create_user(body)
            session.commit()
            return user


async def create_admin(body: CreateUserSchema) -> ShowAdminSchema:
    async with async_session() as session:
        async with session.begin():
            new_user = UserRepository(session)
            user = await new_user.create_admin_user(values=body)
            session.commit()
            return user


async def update_user(updated_params: dict, user_id: UUID) -> Result[User]:
    async with async_session() as session:
        async with session.begin():
            updating_user = UserRepository(session)
            user = await updating_user.get_user_by_id(user_id=user_id)
            updated_user = await updating_user.updated_user(user, **updated_params)
            await session.commit()
            return updated_user


async def deleting_user(user_id: UUID) -> Optional[UUID]:
    async with async_session() as session:
        async with session.begin():
            deleting_user = UserRepository(session)
            deleting_user_id = await deleting_user.delete_user(user_id=user_id)
            session.commit()
            return deleting_user_id
