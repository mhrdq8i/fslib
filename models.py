from typing import List
from sqlmodel import SQLModel, Field, Relationship


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    books: List["Book"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"lazy": "select"}
    )


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(foreign_key="author.id")
    author: Author | None = Relationship(back_populates="books")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
    is_superuser: bool | None = Field(default=False, nullable=False)
