from src.database.config import DatabaseSettings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,AsyncEngine,AsyncSession

from typing import AsyncGenerator

db_settings = DatabaseSettings()

def create_db() -> AsyncEngine:
    url = db_settings.get_db_url
    engine = create_async_engine(url=url)
    return engine

engine = create_db()
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session