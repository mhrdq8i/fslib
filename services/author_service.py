from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models import Author
from schemas import AuthorCreate, AuthorUpdate
from exceptions import NotFoundError, ConflictError


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Author]:
        result = await self.session.exec(select(Author))

        return result.all()

    async def get_by_id(self, author_id: int) -> Author:
        author = await self.session.get(Author, author_id)
        if not author:
            raise NotFoundError(f"Author {author_id} not found")
        return author

    async def create(self, data: AuthorCreate) -> Author:
        # uniqueness check example
        result = await self.session.exec(
            select(Author).where(
                Author.name == data.name
            )
        )
        if result.first():
            raise ConflictError("Author already exists")

        payload = data.model_dump()
        author = Author(**payload)

        self.session.add(author)
        await self.session.commit()
        await self.session.refresh(author)

        return author

    async def update(
        self,
        author_id: int,
        data: AuthorUpdate
    ) -> Author:

        author = await self.get_by_id(author_id)
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(author, k, v)

        self.session.add(author)
        await self.session.commit()
        await self.session.refresh(author)

        return author

    async def delete(self, author_id: int) -> None:
        author = await self.get_by_id(author_id)

        await self.session.delete(author)
        await self.session.commit()
