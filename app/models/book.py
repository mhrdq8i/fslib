from sqlmodel import SQLModel, Field, Relationship


class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: int = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(foreign_key="authors.id")
    author: "Author" = Relationship(
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
