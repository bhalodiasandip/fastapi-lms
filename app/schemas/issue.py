from datetime import datetime
from pydantic import BaseModel


class IssueCreate(BaseModel):
    book_id: int
    user_id: int


class IssueOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    issued_at: datetime
    returned_at: datetime | None

    class Config:
        from_attributes = True
