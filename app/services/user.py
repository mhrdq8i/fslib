from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from exceptions import EntityAlreadyExistsException
from services.auth import get_password_hash


async def create_user(
    session: AsyncSession,
    user_in: User
) -> User:
    result = await session.execute(
        select(User).where(
            User.username == user_in.username
        )
    )
    if result.scalars().first():
        raise EntityAlreadyExistsException("User")

    user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_superuser=user_in.is_superuser
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
