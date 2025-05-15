from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models import Author
from schemas import AuthorCreate
from exceptions import NotFoundError, ConflictError


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Author]:

        result = await self.session.exec(select(Author).options())

        return result.all()

    async def get_by_id(self, author_id: int) -> Author:

        author = await self.session.get(Author, author_id)

        if not author:
            raise NotFoundError(f"Author {author_id} not found")
        return author

    async def create(self, data: AuthorCreate) -> Author:
        # could check for unique name
        existing = await self.session.exec(
            select(Author).where(
                Author.name == data.name
            )
        )

        if existing.first():
            raise ConflictError(
                "Author with this name already exists"
            )

        author = Author.model_validate(data)
        self.session.add(author)

        await self.session.commit()
        await self.session.refresh(author)

        return author

    async def delete(self, author_id: int) -> None:

        author = await self.get_by_id(author_id)

        await self.session.delete(author)
        await self.session.commit()
