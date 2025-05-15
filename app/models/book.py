from sqlmodel import SQLModel, Field, Relationship


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(foreign_key="authors.id")
    author: "Author" = Relationship(back_populates="books")
