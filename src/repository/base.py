from sqlalchemy import select

from src.database.connection import async_session

class BaseRepository:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            stmt = select(cls.model)
            res = await session.execute(stmt)
            return res.scalars().all()
    
    @classmethod
    async def add_one(cls,data):
        async with async_session() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.flush()
            await session.commit()
            return instance.id

    @classmethod
    async def get_one_by_id(cls,id:int, stmt=None):
        async with async_session() as session:
            stmt = select(cls.model).filter_by(id=id) if stmt is None else stmt
            res = await session.execute(stmt)
            return res.scalars().one_or_none()