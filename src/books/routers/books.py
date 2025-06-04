from fastapi import APIRouter

from src.books.repository import BooksRepository
from src.books.schemas import Book, AddBook, CategoriesToBook, Category

from typing import Optional

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/")
async def get_books() -> list[Book]:
    return await BooksRepository.get_all()

@router.post("/add")
async def add_book(data:AddBook) -> int:
    data_dict = data.model_dump()
    return await BooksRepository.add_one(data_dict)

#maybe rewrite on a isbn instead id
@router.get("/{book_id}")
async def get_one(book_id:int)->Optional[Book]:
    return await BooksRepository.get_one_by_id(book_id)
    
#temp router. maybe)
@router.patch("/add-category-to-book")
async def add_categories_to_book(data:CategoriesToBook) -> list[Category]:
    data_as_dict = data.model_dump()
    print(data_as_dict)
    return await BooksRepository.add_categories_to_book(data_as_dict)