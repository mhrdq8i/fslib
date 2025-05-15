from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):

    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalars().first()

    if not user or not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user
