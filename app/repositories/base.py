from typing import Any
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import AbstractBaseModel

Entity = TypeVar("Entity", bound=AbstractBaseModel)


class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, model: Type[Entity]) -> List[Entity]:
        result = await self.db_session.execute(select(model))
        return result.scalars().all()

    async def get_by_id(self, model: Type[Entity], param) -> Optional[Entity]:
        res = await self.db_session.execute(select(model).filter_by(id=param))
        return res.scalar()

    async def create(self, entity) -> Entity:
        self.db_session.add(entity)
        await self.db_session.flush()
        return entity

    async def update(self, model, instance, values: dict) -> Result[Any]:
        res = await self.db_session.execute(
            (update(model).where(model.id == instance.id).values(**values))
        )
        await self.db_session.flush()
        return res

    async def delete(self, model: Type[Entity], instance_id: UUID) -> Optional[UUID]:
        res = await self.db_session.execute(
            delete(model).where(and_(model.id == instance_id)).returning(model.id)
        )
        deleted_entity = res.scalar()
        if deleted_entity is not None:
            await self.db_session.commit()
            return deleted_entity
