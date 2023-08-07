from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from uuid import UUID

from sqlalchemy import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import AbstractBaseModel
from app.models.user import User

Entity = TypeVar("Entity", bound=AbstractBaseModel)


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, stmt: Select) -> List[Entity]:
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, entity: select) -> Optional[User]:
        res = await self.db_session.execute(entity)
        entity = res.scalar()
        if entity is not None:
            await self.db_session.commit()
            return entity

    async def create(self, entity: Type[Entity]) -> Entity:
        self.db_session.add(entity)
        await self.db_session.flush()
        return entity

    async def update(self, entity: Type[Entity]) -> Optional[UUID]:
        res = await self.db_session.execute(entity)
        updated_entity = res.fetchone()
        if updated_entity is not None:
            return updated_entity[0]

    async def delete(self, entity: Type[Entity]) -> Optional[UUID]:
        res = await self.db_session.execute(entity)
        deleted_entity = res.scalar()
        if deleted_entity is not None:
            await self.db_session.commit()
            return deleted_entity
