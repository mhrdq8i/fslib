from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session, engine
from models.user import User
from services.author import AuthorService
from services.book import BookService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_author_service(
    session: AsyncSession = Depends(get_session)
) -> AuthorService:
    return AuthorService(session)


async def get_book_service(
    session: AsyncSession = Depends(get_session)
) -> BookService:
    return BookService(session)


async def get_user(username: str) -> User:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(User).where(
                User.username == username
            )
        )
        return result.scalars().first()


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if user.password != password:  # Plain text comparison
        return False
    return user
