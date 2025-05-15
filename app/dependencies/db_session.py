from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from services.author import AuthorService
from services.book import BookService


async def get_author_service(
    session: AsyncSession = Depends(get_session)
) -> AuthorService:
    return AuthorService(session)


async def get_book_service(
    session: AsyncSession = Depends(get_session)
) -> BookService:
    return BookService(session)
