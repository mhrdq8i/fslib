from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    username: str = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    full_name: str
    disabled: bool | None = Field(default=False)
