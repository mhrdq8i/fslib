from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.author import Author
from schemas.author import AuthorCreate, AuthorUpdate
from exceptions import EntityNotFoundException


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_author(self, author: AuthorCreate) -> Author:
        db_author = Author(**author.model_dump())
        self.session.add(db_author)
        await self.session.commit()
        await self.session.refresh(db_author)
        return db_author

    async def get_author(self, author_id: int) -> Author:
        author = await self.session.get(Author, author_id)
        if not author:
            raise EntityNotFoundException("Author", author_id)
        return author

    async def get_all_authors(self) -> list[Author]:
        result = await self.session.execute(select(Author))
        return result.scalars().all()

    async def update_author(
        self,
            author_id: int,
            update: AuthorUpdate
    ) -> Author:
        author = await self.get_author(author_id)
        update_data = update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(author, key, value)
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def delete_author(self, author_id: int) -> bool:
        author = await self.get_author(author_id)
        await self.session.delete(author)
        await self.session.commit()
        return True
