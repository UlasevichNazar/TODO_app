from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from config.config import setting

engine = create_async_engine(setting.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
