from fastapi import APIRouter

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/")
async def get_books():
    pass