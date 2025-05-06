from fastapi import APIRouter

from src.authors.schemas import AddAuthor, Author
from src.authors.repository import AuthorsRepository

router = APIRouter(
    prefix="/authors",
    tags=["Authors"])


@router.get("/")
async def get_all() -> list[Author]:
    return await AuthorsRepository.get_all()

@router.get("/{author_id}")
async def get_one(author_id:int) -> Author:
    return await AuthorsRepository.get_one_by_id(author_id)

@router.get("/{author_id}/all")
async def get_all_authors_books(author_id:int):
    pass

@router.post("/add")
async def add_one(data:AddAuthor) -> int:
    data_as_dict = data.model_dump()
    return await AuthorsRepository.add_one(data_as_dict)
