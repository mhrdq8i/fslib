from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    bio: str


class AuthorRead(AuthorCreate):
    id: int

    class Config:
        orm_mode = True


class AuthorUpdate(BaseModel):
    name: str | None
    bio: str | None
