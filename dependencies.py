from jwt import PyJWTError, decode, encode
from datetime import datetime, timedelta, timezone

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings
from exceptions import (
    AuthenticationError,
    NotSuperUserError
)
from database import get_session
from models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:

    credentials_exception = AuthenticationError(
        "Could not validate credentials"
    )
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    result = await session.exec(
        select(User).where(
            User.username == username
        )
    )
    user = result.one_or_none()
    if not user:
        raise credentials_exception

    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise NotSuperUserError()
    return current_user


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    to_encode = data.copy()
    to_encode.update({"iat": now, "exp": expire})

    return encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
