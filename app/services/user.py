from typing import List
from typing import Optional
from uuid import UUID

from app.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema
from app.schemas.user import ShowUserSchema
from app.services.hashing import Hasher
from database.database import async_session


async def get_all_users() -> List[ShowUserSchema]:
    async with async_session() as session:
        user_repo = UserRepository(session)
        users = await user_repo.get_all_users()
        return users


async def get_user(user_id: UUID) -> Optional[ShowUserSchema]:
    async with async_session() as session:
        async with session.begin():
            getting_user = UserRepository(session)
            user = await getting_user.get_user_by_id(user_id)
            if user is not None:
                return ShowUserSchema(
                    id=user_id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                )


async def get_user_by_username_for_auth(username: str):
    async with async_session() as session:
        async with session.begin():
            user = UserRepository(session)
            return await user.get_user_by_username(username=username)


async def create_new_user(body: CreateUserSchema) -> ShowUserSchema:
    async with async_session() as session:
        async with session.begin():
            new_user = UserRepository(session)
            user = await new_user.create_user(
                username=body.username,
                email=body.email,
                password=Hasher.get_password_hash(body.password),
            )
            return ShowUserSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
            )


async def update_user(updated_user_params: dict, user_id: UUID) -> Optional[UUID]:
    async with async_session() as session:
        async with session.begin():
            updating_user = UserRepository(session)
            user = await updating_user.updated_user(
                user_id=user_id, **updated_user_params
            )
            return user


async def deleting_user(user_id: UUID) -> Optional[UUID]:
    async with async_session() as session:
        async with session.begin():
            deleting_user = UserRepository(session)
            deleting_user_id = await deleting_user.delete_user(user_id=user_id)
            return deleting_user_id