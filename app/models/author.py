from sqlmodel import SQLModel, Field, Relationship
from typing import List


class Author(SQLModel, table=True):
    __tablename__ = "authors"
    id: int = Field(default=None, primary_key=True)
    name: str
    bio: str
    books: List["Book"] = Relationship(back_populates="author")
