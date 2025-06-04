from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.connection import async_session

from src.repository.base import BaseRepository
from src.authors.models import Authors

class AuthorsRepository(BaseRepository):
    model = Authors

    @classmethod
    async def get_authors_books(cls,author_id):
        async with async_session() as session:
            stmt = select(Authors).options(selectinload(Authors.books)).where(Authors.id==author_id)
            res = await session.execute(stmt)
            authors_with_books = res.scalars().one_or_none()
            print(authors_with_books)
            print(authors_with_books.books)
            return authors_with_books