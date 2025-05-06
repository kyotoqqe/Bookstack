from src.repository.base import BaseRepository
from src.books.models import Books


class BooksRepository(BaseRepository):
    model = Books
