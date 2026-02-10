from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.core.database import Base


class UserType(enum.Enum):
    student = "student"
    teacher = "teacher"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    user_type: Mapped[UserType] = mapped_column(
        Enum(UserType), nullable=False
    )
