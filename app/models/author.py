from sqlmodel import SQLModel, Field, Relationship
from typing import List


class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    books: List["Book"] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
