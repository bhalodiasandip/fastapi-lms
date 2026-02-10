from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.models.admin import Admin
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Admin).where(Admin.email == form_data.username))
    admin = result.scalar_one_or_none()

    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    data = {"sub": str(admin.id)}

    return Token(
        access_token=create_access_token(data),
        refresh_token=create_refresh_token(data),
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    from jose import jwt, JWTError
    from app.core.config import settings

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload["sub"]
        data = {"sub": user_id}

        return Token(
            access_token=create_access_token(data),
            refresh_token=create_refresh_token(data),
        )

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
