from fastapi import APIRouter

from src.books.schemas import AddCategory, Category, CategoryWithCounts
from src.books.repository import CategoriesRepository

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/")
async def get_categories() -> list[Category]:
    return await CategoriesRepository.get_all()

@router.post("/add")
async def add_category(data:AddCategory) -> int:
    data_as_dict = data.model_dump()
    return await CategoriesRepository.add_one(data_as_dict)



#router on single

@router.get("/category_stats")
async def get_category_stats() -> list[CategoryWithCounts]:
    return await CategoriesRepository.categories_books_count()