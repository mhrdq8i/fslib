from pydantic import BaseModel
from typing import List


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class BookRef(BaseModel):
    id: int
    title: str


class AuthorRead(AuthorBase):
    id: int
    books: List[BookRef] = []
