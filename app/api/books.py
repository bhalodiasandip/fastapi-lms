from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from app.schemas.book import BookCreate, BookRead

router = APIRouter(prefix="/books", tags=["Books"])

@router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    payload: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    author = await db.get(Author, payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    result = await db.execute(
        select(Category).where(Category.id.in_(payload.category_ids))
    )
    categories = result.scalars().all()

    if len(categories) != len(payload.category_ids):
        raise HTTPException(status_code=400, detail="Invalid categories")

    book = Book(
        title=payload.title,
        author_id=payload.author_id,
        categories=categories,
    )

    db.add(book)
    await db.commit()

    result = await db.execute(
        select(Book)
        .where(Book.id == book.id)
        .options(selectinload(Book.categories)) #selectinload: Avoids the N+1 problem
    )
    book = result.scalar_one()

    return BookRead(
        id=book.id,
        title=book.title,
        author_id=book.author_id,
        categories=[c.name for c in book.categories],
    )


@router.get(
    "",
    response_model=list[BookRead],
)
async def list_books(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Book).options(selectinload(Book.categories))
    )
    books = result.scalars().all()    
    return [
        BookRead(
            id=book.id,
            title=book.title,
            author_id=book.author_id,
            categories=[c.name for c in book.categories],
        )
        for book in books
    ]

@router.get(
    "/{book_id}",
    response_model=BookRead,
)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Book)
        .where(Book.id == book_id)
        .options(selectinload(Book.categories))
    )
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return BookRead(
        id=book.id,
        title=book.title,
        author_id=book.author_id,
        categories=[c.name for c in book.categories],
    )

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    await db.delete(book)
    await db.commit()
