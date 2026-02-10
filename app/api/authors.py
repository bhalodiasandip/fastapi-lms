from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorRead

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/secure-data")
async def secure(admin=Depends(get_current_admin)):
    return {"msg": f"Hello {admin.email}"}

@router.post(
    "",
    response_model=AuthorRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_author(
    payload: AuthorCreate,
    db: AsyncSession = Depends(get_db),
):
    author = Author(name=payload.name)
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


@router.get(
    "",
    response_model=list[AuthorRead],
)
async def list_authors(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Author))
    return result.scalars().all()


@router.get(
    "/{author_id}",
    response_model=AuthorRead,
)
async def get_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
):
    author = await db.get(Author, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return author


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
):
    author = await db.get(Author, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    await db.delete(author)
    await db.commit()
