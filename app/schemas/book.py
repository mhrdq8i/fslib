from typing import Optional

from pydantic import BaseModel
from schemas.author import AuthorRead


class BookCreate(BaseModel):
    title: str
    author_id: int


class BookRead(BookCreate):
    id: int
    author: "AuthorRead"

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
