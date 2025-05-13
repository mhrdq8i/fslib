from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from models.book import Book
from schemas.book import BookCreate
from exceptions import EntityNotFoundException


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_book(self, book: BookCreate) -> Book:
        db_book = Book(**book.model_dump())
        self.session.add(db_book)
        await self.session.commit()
        await self.session.refresh(db_book)

        return db_book

    async def get_book(self, book_id: int) -> Book:
        book = await self.session.get(Book, book_id)
        if not book:
            raise EntityNotFoundException("Book", book_id)
        await self.session.refresh(
            book,
            attribute_names=["author"]
        )

        return book

    async def get_all_books(self) -> list[Book]:
        result = await self.session.execute(
            select(Book).options(joinedload(Book.author))
        )
        return result.scalars().all()

    async def get_books_by_author(self, author_id: int) -> list[Book]:
        result = await self.session.execute(
            select(Book)
            .where(Book.author_id == author_id)
            .options(joinedload(Book.author))
        )

        return result.scalars().all()
