from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models import Book, Author
from schemas import BookCreate, BookUpdate
from exceptions import NotFoundError


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Book]:
        result = await self.session.exec(select(Book))

        return result.all()

    async def get_by_id(self, book_id: int) -> Book:
        book = await self.session.get(Book, book_id)
        if not book:
            raise NotFoundError(f"Book {book_id} not found")

        return book

    async def create(self, data: BookCreate) -> Book:
        # 1. Ensure the author exists
        author = await self.session.get(Author, data.author_id)
        if not author:
            raise NotFoundError(f"Author {data.author_id} not found")

        # 2. Create the book
        payload = data.model_dump()  # or data.dict()
        book = Book(**payload)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def update(self, book_id: int, data: BookUpdate) -> Book:
        book = await self.get_by_id(book_id)
        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(book, field, value)

        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)

        return book

    async def delete(self, book_id: int) -> None:
        book = await self.get_by_id(book_id)
        await self.session.delete(book)
        await self.session.commit()
