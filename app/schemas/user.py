from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    is_superuser: bool = False


class UserRead(UserBase):
    id: int
    is_superuser: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
