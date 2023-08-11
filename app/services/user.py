from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from app.models.user import Roles
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserSchema
from app.schemas.user import ShowAdminSchema
from app.schemas.user import ShowUserSchema
from app.schemas.user import UpdateUserRequestSchema
from app.services.hashing import Hasher
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
            user = await new_user.create_user(
                username=body.username,
                email=body.email,
                password=Hasher.get_password_hash(body.password),
                roles=[
                    Roles.ROLE_USER,
                ],
            )
            return ShowUserSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
            )


async def create_admin(body: CreateUserSchema) -> ShowAdminSchema:
    async with async_session() as session:
        async with session.begin():
            new_user = UserRepository(session)
            user = await new_user.create_user(
                username=body.username,
                email=body.email,
                password=Hasher.get_password_hash(body.password),
                roles=[
                    Roles.ROLE_ADMIN,
                ],
            )
            return ShowAdminSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                roles=user.roles,
            )


async def update_user(body: UpdateUserRequestSchema, user_id: UUID):
    async with async_session() as session:
        async with session.begin():
            updating_user = UserRepository(session)
            user = await updating_user.get_user_by_id(user_id=user_id)
            await updating_user.updated_user(user, body.model_dump())
            await session.commit()
            return None


async def deleting_user(user_id: UUID) -> Optional[UUID]:
    async with async_session() as session:
        async with session.begin():
            deleting_user = UserRepository(session)
            deleting_user_id = await deleting_user.delete_user(user_id=user_id)
            return deleting_user_id
