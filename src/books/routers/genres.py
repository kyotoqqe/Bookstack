from typing import Optional

from fastapi import APIRouter

from src.books.repository import GenresRepository
from src.books.schemas import AddGenre, Genre, GenreBooks,GenreWithCounts

router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)

@router.get("/")
async def get_all() -> list[Optional[Genre]]:
    return await GenresRepository.get_all()

@router.post("/add")
async def add_one(data:AddGenre) -> int:
    data_as_dict = data.model_dump()
    return await GenresRepository.add_one(data_as_dict)

@router.get("/{genre_id}/all")
async def get_genre_books(genre_id:int) -> GenreBooks:
    return await GenresRepository.get_all_books_by_genre(genre_id)

@router.get("/genres_stats")
async def get_genres_stats() -> list[GenreWithCounts]:
    orm_result = await GenresRepository.genre_books_count()
    return GenreWithCounts.build(orm_result)