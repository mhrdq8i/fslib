from jose import jwt, JWTError

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.config import settings
from models.user import User
from exceptions import (
    UnauthorizedException,
    ForbiddenException
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get_db() -> AsyncSession:
    async with get_session() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings().SECRET_KEY,
            algorithms=[settings().ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            raise UnauthorizedException()

        result = await session.execute(
            select(User).where(
                User.username == username
            )
        )
        user = result.scalars().first()

        if not user:
            raise UnauthorizedException()

        return user
    except JWTError:
        raise UnauthorizedException()


async def get_current_active_superuser(
        current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        raise ForbiddenException()

    return current_user
