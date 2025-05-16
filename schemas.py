from pydantic import BaseModel, constr
from typing import List


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


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class PasswordResetRequest(BaseModel):
    """
    Body for requesting a password reset.
    """
    email: str


class PasswordResetConfirm(BaseModel):
    """
    Body for confirming a reset with the token + new password.
    """
    token: str
    new_password: constr(min_length=8)
