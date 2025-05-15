from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models.author import Author as AuthorModel
from schemas.author import AuthorRead, AuthorCreate
from schemas.book import BookRef
from exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException
)


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_authors(self) -> list[AuthorRead]:
        result = await self.session.execute(
            select(AuthorModel).options(selectinload(AuthorModel.books))
        )
        authors = result.scalars().all()
        return [self._to_read_schema(author) for author in authors]

    async def get_author(self, author_id: int) -> AuthorRead:
        result = await self.session.execute(
            select(AuthorModel)
            .options(selectinload(AuthorModel.books))
            .where(AuthorModel.id == author_id)
        )
        author = result.scalars().first()
        if not author:
            raise EntityNotFoundException("Author", author_id)

        return self._to_read_schema(author)

    async def create_author(self, author_in: AuthorCreate) -> AuthorRead:
        # Check for existing author
        result = await self.session.execute(
            select(AuthorModel).where(AuthorModel.name == author_in.name)
        )
        if result.scalars().first():
            raise EntityAlreadyExistsException("Author")

        db_author = AuthorModel(**author_in.dict())
        self.session.add(db_author)
        await self.session.commit()
        await self.session.refresh(db_author)

        return self._to_read_schema(db_author)

    def _to_read_schema(self, author: AuthorModel) -> AuthorRead:
        return AuthorRead(
            id=author.id,
            name=author.name,
            books=[
                BookRef(
                    id=book.id, title=book.title
                )
                for book in author.books
            ]
        )
