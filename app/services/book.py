# services/book.py
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.book import Book
from schemas.book import BookCreate, BookUpdate


async def create_book(session: AsyncSession, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book


async def get_books(session: AsyncSession) -> list[Book]:
    result = await session.execute(
        select(Book).options(joinedload(Book.author))
    )

    return result.scalars().all()


async def update_book(
    session: AsyncSession,
    book_id: int,
    book_update: BookUpdate
) -> Book:

    book = await session.get(Book, book_id)
    if not book:
        raise ValueError("Book not found")

    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    await session.commit()
    await session.refresh(book)

    return book


async def delete_book(session: AsyncSession, book_id: int) -> bool:
    book = await session.get(Book, book_id)
    if book:
        await session.delete(book)
        await session.commit()
        return True
    return False
