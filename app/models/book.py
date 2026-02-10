from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    is_available: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="books",
        lazy="selectin",
        # we can define foreign_keys parameter. default it will detect automatically, if only one relationship between author and book.
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="book_categories",
        back_populates="books",
        lazy="selectin",
    )