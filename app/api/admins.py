# app/api/admins.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminRead
from app.core.security import hash_password

router = APIRouter(prefix="/admins", tags=["Admins"])


@router.post("", response_model=AdminRead, status_code=status.HTTP_201_CREATED)
async def create_admin(
    payload: AdminCreate,
    db: AsyncSession = Depends(get_db),
):
    # 1️⃣ Check if admin already exists
    result = await db.execute(select(Admin).where(Admin.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")

    # 2️⃣ Hash password
    password_hash = hash_password(payload.password)

    # 3️⃣ Create Admin object
    admin = Admin(
        email=payload.email,
        password_hash=password_hash,
        is_superuser=payload.is_superuser if hasattr(payload, "is_superuser") else False,
    )

    db.add(admin)
    await db.commit()
    await db.refresh(admin)

    return admin
