from typing import Optional
from datetime import date

from sqlalchemy import Computed, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Authors(Base):
    __tablename__ = "authors"
    id:Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(String(50))
    middle_name:Mapped[str] = mapped_column(String(50), nullable=True)
    last_name:Mapped[str] = mapped_column(String(50))
    biography:Mapped[Optional[str]] = mapped_column(Text)
    date_of_birth:Mapped[date] = mapped_column(Date)
    date_of_death:Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    books:Mapped[list["Books"]] = relationship(
        back_populates="author"
    )
    