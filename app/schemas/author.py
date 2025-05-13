from typing import Optional

from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    bio: str


class AuthorRead(AuthorCreate):
    id: int

    class Config:
        from_attributes = True


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
