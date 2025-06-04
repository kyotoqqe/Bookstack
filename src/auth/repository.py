from typing import Optional

from sqlalchemy import select, delete

from src.repository.base import BaseRepository
from src.auth.models import Users, RefreshSessions
from src.database.connection import async_session

from uuid import uuid4

REFRESH_TOKEN_EXPIRE_DAYS = 30

class UsersRepository(BaseRepository):
    model=Users

    @classmethod
    async def activate_user(cls,user_id:int) -> Optional[Users]:
        async with async_session() as session:
            user = await super().get_one_by_id(user_id)
            if user:
                session.add(user)
                user.active = True
                await session.commit()
            return user
    
    @classmethod 
    async def get_user(cls, **kwargs) -> Optional[Users]:
        async with async_session() as session:
            stmt = select(Users).filter_by(**kwargs)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
    
    @classmethod
    async def change_password(cls, user_id:int, password:str):
        async with async_session() as session:
            user = await super().get_one_by_id(user_id)
            if user:
                session.add(user)
                user.password = password
                await session.commit()


class RefreshSessionsRepository(BaseRepository):
    model=RefreshSessions

    @classmethod
    async def create(cls, user_id):
        async with async_session() as session:
            refresh = RefreshSessions(user_id=user_id,
                                      refresh_token=uuid4(),
                                      expires_in = REFRESH_TOKEN_EXPIRE_DAYS)
            session.add(refresh)
            await session.commit()
            return refresh.refresh_token
        
    @classmethod 
    async def get_session(cls, **kwargs) -> Optional[RefreshSessions]:
        async with async_session() as session:
            stmt = select(RefreshSessions).filter_by(**kwargs)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
    
    @classmethod
    async def delete(cls, refresh_token):
        async with async_session() as session:
            stmt = delete(RefreshSessions).where(RefreshSessions.refresh_token==refresh_token)
            await session.execute(stmt)
    
    @classmethod
    async def clear_all_sessions_for_user(cls, user_id:int):
        async with async_session() as session:
            stmt = delete(RefreshSessions).filter(user_id=user_id)
            await session.execute(stmt)
   
