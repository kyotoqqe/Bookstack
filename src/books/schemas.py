from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.isbn import ISBN

from datetime import date
from typing import Optional


class AddBook(BaseModel):
    title:str = Field(max_length=256)
    description:Optional[str] = None
    isbn:ISBN
    year_of_publish:date

class Book(AddBook):
    id:int
    model_config = ConfigDict(from_attributes=True)