from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models.author import Author as AuthorModel
from models.book import Book as BookModel
from schemas.book import BookRead, BookCreate, AuthorRef
from exceptions import EntityNotFoundException


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_books(self) -> list[BookRead]:
        result = await self.session.execute(
            select(BookModel).options(selectinload(BookModel.author))
        )
        books = result.scalars().all()
        return [self._to_read_schema(book) for book in books]

    async def get_book(self, book_id: int) -> BookRead:
        result = await self.session.execute(
            select(BookModel)
            .options(selectinload(BookModel.author))
            .where(BookModel.id == book_id)
        )
        book = result.scalars().first()
        if not book:
            raise EntityNotFoundException("Book", book_id)
        return self._to_read_schema(book)

    async def create_book(self, book_in: BookCreate) -> BookRead:
        # Verify author exists
        result = await self.session.execute(
            select(AuthorModel).where(AuthorModel.id == book_in.author_id)
        )
        if not result.scalars().first():
            raise EntityNotFoundException("Author", book_in.author_id)

        db_book = BookModel(**book_in.model_dump())
        self.session.add(db_book)
        await self.session.commit()
        await self.session.refresh(db_book)
        return self._to_read_schema(db_book)

    def _to_read_schema(self, book: BookModel) -> BookRead:
        return BookRead(
            id=book.id,
            title=book.title,
            author_id=book.author_id,
            author=AuthorRef(
                id=book.author.id,
                name=book.author.name)
            if book.author else None
        )
