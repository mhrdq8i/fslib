from pydantic import BaseModel, constr
from typing import Optional, List

# Users


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    is_superuser: Optional[bool] = None

# Auth tokens


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Authors


class BookRead(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    name: str


class AuthorRead(BaseModel):
    id: int
    name: str
    books: List[BookRead] = []

    class Config:
        orm_mode = True


class AuthorUpdate(BaseModel):
    name: Optional[str] = None

# Book


class BookCreate(BaseModel):
    title: str
    author_id: int


class BookRead(BaseModel):
    id: int
    title: str
    author_id: int

    class Config:
        orm_mode = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None


# Password reset


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=8)
