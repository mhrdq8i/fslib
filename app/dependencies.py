from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.database import get_session
from services.author import AuthorService
from services.book import BookService

from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_author_service(
    session: AsyncSession = Depends(get_session)
) -> AuthorService:
    return AuthorService(session)


async def get_book_service(
    session: AsyncSession = Depends(get_session)
) -> BookService:
    return BookService(session)


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe"
    )


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> User:
    user = fake_decode_token(token)
    return user
