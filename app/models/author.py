from sqlmodel import SQLModel, Field, Relationship
from typing import List


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    books: List["Book"] = Relationship(back_populates="author")
