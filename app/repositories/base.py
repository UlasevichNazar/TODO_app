from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar

from sqlalchemy import Result
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import AbstractBaseModel

Entity = TypeVar("Entity", bound=AbstractBaseModel)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_all(self, model: Type[Entity]):
        result = await self.session.execute(select(model))
        return result.scalars().all()

    async def _get(self, model: Type[Entity], param) -> Optional[Entity]:
        res = await self.session.execute(select(model).filter_by(id=param))
        return res.scalar()

    async def _create(self, entity) -> Entity:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def _update(self, model, instance, values: dict) -> Result[Any]:
        res = await self.session.execute(
            (update(model).where(model.id == instance.id).values(**values))
        )
        await self.session.flush()
        return res

    async def _delete(self, instance) -> None:
        res = await self.session.delete(instance)
        await self.session.flush()
        return res
