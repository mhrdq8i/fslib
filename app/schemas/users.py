from pydantic import BaseModel


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
    username: str | None = None
    is_superuser: bool | None = None
