from pydantic import BaseModel


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
    # books: List[BookRead] = []

    class Config:
        orm_mode = True


class AuthorUpdate(BaseModel):
    name: str | None = None
