from fastapi import FastAPI

from src.books.router import router as books_router
from src.authors.routers import router as authors_router

app = FastAPI()
app.include_router(books_router)
app.include_router(authors_router)
#put all routers to __init__.py and create global router and this router connect to app