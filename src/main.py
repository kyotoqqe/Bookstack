from fastapi import FastAPI

from src.books.routers.books import router as books_router
from src.books.routers.genres import router as genre_router
from src.books.routers.categories import router as category_router

from src.authors.routers import router as authors_router

from src.auth.routers import router as auth_router


app = FastAPI()
app.include_router(books_router)
app.include_router(genre_router)
app.include_router(category_router)
app.include_router(authors_router)
app.include_router(auth_router)
#put all routers to __init__.py and create global router and this router connect to app