from typing import Optional
from datetime import date

from pydantic import BaseModel,Field, ConfigDict

from src.books.schemas import Book

class AddAuthor(BaseModel):
    first_name:str = Field(max_length=50)
    middle_name:str = Field(max_length=50)
    last_name:str = Field(max_length=50)
    biography:Optional[str] = None
    date_of_birth:date
    date_of_death:Optional[date] = None

class Author(AddAuthor):
    id:int
    model_config = ConfigDict(from_attributes=True)

class AuthorBooks(Author):
    books:list[Optional[Book]]