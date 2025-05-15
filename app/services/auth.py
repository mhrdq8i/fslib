from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: timedelta = None
) -> str:

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings().SECRET_KEY,
        algorithm=settings().ALGORITHM
    )


async def authenticate_user(
    session: AsyncSession,
    username: str,
    password: str
) -> Optional[User]:

    result = await session.execute(
        select(User).where(
            User.username == username
        )
    )
    user = result.scalars().first()

    if not user or not verify_password(
        password,
        user.hashed_password
    ):
        return None
    return user
