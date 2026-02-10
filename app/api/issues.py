from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func

from app.core.database import get_db
from app.models.issue import Issue
from app.models.book import Book
from app.schemas.issue import IssueCreate, IssueOut

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.post(
    "/",
    response_model=IssueOut,
    status_code=status.HTTP_201_CREATED,
)
async def issue_book(
    payload: IssueCreate,
    db: AsyncSession = Depends(get_db),
):
    book = await db.get(Book, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.is_available:
        raise HTTPException(
            status_code=400,
            detail="Book is already issued",
        )

    issue = Issue(
        book_id=payload.book_id,
        user_id=payload.user_id,
    )

    book.is_available = False

    db.add(issue)
    await db.commit()
    await db.refresh(issue)

    return issue


@router.post(
    "/{issue_id}/return",
    response_model=IssueOut,
)
async def return_book(
    issue_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Issue).where(Issue.id == issue_id)
    )
    issue = result.scalar_one_or_none()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if issue.returned_at is not None:
        raise HTTPException(
            status_code=400,
            detail="Book already returned",
        )

    book = await db.get(Book, issue.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    issue.returned_at = func.now()
    book.is_available = True

    await db.commit()
    await db.refresh(issue)

    return issue
