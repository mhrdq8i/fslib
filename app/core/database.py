from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlmodel import SQLModel

from models.user import User
from core.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSessionLocal() as session:
        from services.auth import get_password_hash

        super_username = settings.SUPER_ADMIN_USERNAME
        super_password = settings.SUPER_ADMIN_PASSWORD

        result = await session.execute(
            select(User).where(
                User.username == super_username
            )
        )

        super_user = result.scalars().first()

        if not super_user:
            hashed = get_password_hash(super_password)
            db_user = User(
                username=super_username,
                hashed_password=hashed
            )
            session.add(db_user)
            await session.commit()
