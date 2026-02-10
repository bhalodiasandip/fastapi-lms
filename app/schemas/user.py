from pydantic import BaseModel, EmailStr
from enum import Enum


class UserType(str, Enum):
    student = "student"
    teacher = "teacher"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    user_type: UserType


class UserOut(UserCreate):
    id: int

    class Config:
        from_attributes = True
