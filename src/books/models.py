from src.database.base import Base

from sqlalchemy import String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column

from typing import Optional
from datetime import date

class Books(Base):
    __tablename__ = "books"
    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(String(256))
    description:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    isbn:Mapped[str] = mapped_column(String(17),unique=True)
    year_of_publish:Mapped[date] = mapped_column(Date)
