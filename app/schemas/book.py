from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    author_id: int


class BookCreate(BookBase):
    pass


class AuthorRef(BaseModel):
    id: int
    name: str


class BookRead(BookBase):
    id: int
    author: Optional[AuthorRef] = None
