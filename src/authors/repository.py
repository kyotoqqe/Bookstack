from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.connection import async_session

from src.repository.base import BaseRepository
from src.authors.models import Authors

class AuthorsRepository(BaseRepository):
    model = Authors

    async def get_authors_books(cls,author_id):
        async with async_session() as session:
            stmt = select(Authors).options(joinedload(Authors.books)).where(Authors.id==author_id)
            res = await session.execute(stmt)
            return res.unique().scalars().all()