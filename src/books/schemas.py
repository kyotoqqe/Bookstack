from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.isbn import ISBN

from datetime import date
from typing import Optional


class AddBook(BaseModel):
    title:str = Field(max_length=256)
    description:Optional[str] = None
    isbn:ISBN
    year_of_publish:date
    genre_id:Optional[int] = None
    author_id:int
    #add categories

class Book(AddBook):
    id:int
    categories:list[Optional["Category"]]
    model_config = ConfigDict(from_attributes=True)

class AddGenre(BaseModel):
    title:str

class Genre(AddGenre):
    id:int
    model_config = ConfigDict(from_attributes=True)

class GenreBooks(Genre):
    books:list[Optional[Book]]
    
class GenreWithCounts(Genre):
    books_count:int

    @classmethod
    def build(cls,data:list[tuple[Genre,int]]) -> list["GenreWithCounts"]:
        return [
            GenreWithCounts(
                title = genre.title,
                id = genre.id,
                books_count=count
            ) for genre,count in data
        ]
   
class AddCategory(BaseModel):
    title:str = Field(max_length=50)
    description:Optional[str] = None

class Category(AddCategory):
    id:int

class CategoryWithCounts(BaseModel):
    id:int
    title:str = Field(max_length=255)
    count:int

#temp
class CategoriesToBook(BaseModel):
    book_id:int
    categories_id:list[int]