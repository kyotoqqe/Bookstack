from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.repository.base import BaseRepository
from src.books.models import Books, Genres, Categories, books_categories

from src.database.connection import async_session

class BooksRepository(BaseRepository):
    model = Books

    @classmethod
    async def get_one_by_id(cls,id:int):
        stmt = select(Books).where(Books.id == id).options(selectinload(Books.categories))
        return await super().get_one_by_id(id,stmt)
    
    async def add_categories_to_book(data):
        async with async_session() as session:
            stmt1 = select(Books)\
                .where(Books.id == data["book_id"])\
                .options(selectinload(Books.categories))
            stmt2 = select(Categories).where(Categories.id.in_(data["categories_id"]))

            book = await session.scalar(stmt1)
            categories = await session.scalars(stmt2)

            for category in categories.all():
                book.categories.append(category)

            await session.commit()
            return book.categories
        



class GenresRepository(BaseRepository):
    model = Genres

    @classmethod
    async def get_all_books_by_genre(cls,genre_id:int):
        async with async_session() as session:
            stmt = select(Genres).options(selectinload(Genres.books)).where(Genres.id==genre_id)
            res = await session.execute(stmt)
            return res.scalars().one_or_none()
    
    @classmethod
    async def genre_books_count(cls):
        async with async_session() as session:
            stmt = select(
                Genres, 
                func.count(Books.id).label("books_count"))\
                .join(Books,isouter=True)\
                .group_by(Genres.id)\
                .order_by(func.count(Books.id).desc())
            res = await session.execute(stmt)
            return res.all()

class CategoriesRepository(BaseRepository):
    model = Categories

    @classmethod
    async def categories_books_count(cls):
        async with async_session() as session:
            stmt = select(
                Categories.id,
                Categories.title, 
                func.count(books_categories.c.book_id)
                )\
                .join(books_categories,isouter=True)\
                .group_by(Categories.id)\
                .order_by(func.count(books_categories.c.book_id).desc())
            
            res = await session.execute(stmt)
            category_books = res.all()
            return category_books
        
    #rewrite on sql and after with orm