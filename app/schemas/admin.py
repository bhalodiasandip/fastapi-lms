# app/schemas/admin.py

from pydantic import BaseModel, EmailStr


# Input schema (API request)
class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    is_superuser: bool = False


# Output schema (API response)
class AdminRead(BaseModel):
    id: int
    email: EmailStr
    is_superuser: bool

    model_config = {
        "from_attributes": True
    }
