from sqlmodel import SQLModel, Field, Relationship


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author_id: int | None = Field(
        default=None,
        foreign_key="author.id"
    )
    author: "Author" = Relationship(
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
