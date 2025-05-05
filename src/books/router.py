from fastapi import APIRouter,Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.schemas import Book,AddBook
from src.books.models import Books
from src.database.connection import get_session

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/")
async def get_books(session:AsyncSession=Depends(get_session)):
    stmt = select(Books)
    res = await session.execute(stmt)
    books_models = res.scalars().all()
    books_schemas:list[Book] = [Book.model_validate(book) for book in books_models]
    return books_schemas

@router.post("/add")
async def add_book(data:AddBook, session:AsyncSession=Depends(get_session)):
    book_as_dict = data.model_dump()
    book = Books(**book_as_dict)
    session.add(book)
    session.flush()
    await session.commit()
    return book.id