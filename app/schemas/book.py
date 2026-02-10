from pydantic import BaseModel, Field
from typing import List


class BookBase(BaseModel):
    title: str = Field(..., max_length=255)
    author_id: int
    category_ids: List[int]


class BookCreate(BookBase):
    pass


class BookRead(BaseModel):
    id: int
    title: str
    author_id: int
    categories: list[str]

    model_config = {
        "from_attributes": True
    }

class BookOut(BaseModel):
    id: int
    title: str
    author_id: int
    is_available: bool

    class Config:
        from_attributes = True