from pydantic import BaseModel, Field
from pydantic_extra_types.isbn import ISBN

from datetime import date
from typing import Optional

class Book(BaseModel):
    id:int
    title:str = Field(max_length=256)
    description:Optional[str] = None
    isbn:ISBN
    year_of_publish:date