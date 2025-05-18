from pydantic import BaseModel


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
    title: str | None = None
    author_id: int | None = None
