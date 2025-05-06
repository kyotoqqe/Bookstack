from src.database.base import Base

from sqlalchemy import Table, Column, ForeignKey, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Optional
from datetime import date

#maybe create file like associatation table or related shit for save tables like this

books_categories = Table(
    "books_categories",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"),primary_key=True)
)

class Books(Base):
    __tablename__ = "books"
    id:Mapped[int] = mapped_column(primary_key=True) #create separate class with id or create annotation
    title:Mapped[str] = mapped_column(String(255))
    description:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    isbn:Mapped[str] = mapped_column(String(17),unique=True)
    year_of_publish:Mapped[date] = mapped_column(Date)
    genre_id:Mapped[Optional[int]] = mapped_column(ForeignKey("genres.id", ondelete="SET NULL"), nullable=True) #add cascade setnull
    author_id:Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))

    categories:Mapped[list["Categories"]] = relationship(
        secondary=books_categories, back_populates="books"
    )
    genre:Mapped["Genres"] = relationship(
        back_populates="books" 
    )

    author:Mapped["Authors"] = relationship(
        back_populates="books"
    )

class Categories(Base):
    __tablename__ = "categories"
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(255))
    description:Mapped[Optional[str]] = mapped_column(String(255))

    books:Mapped[list["Books"]] = relationship(
        secondary=books_categories, back_populates="categories"
    )


class Genres(Base):
    __tablename__ = "genres"
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(256))

    books:Mapped[list["Books"]] = relationship(
        back_populates="genre"
    )