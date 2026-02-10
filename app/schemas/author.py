from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str = Field(..., max_length=255)


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    model_config = {
        "from_attributes": True
    }
