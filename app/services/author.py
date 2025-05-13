# services/author.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.author import Author
from schemas.author import AuthorCreate, AuthorUpdate


async def create_author(session: AsyncSession, author: AuthorCreate) -> Author:
    db_author = Author(**author.model_dump())
    session.add(db_author)
    await session.commit()
    await session.refresh(db_author)

    return db_author


async def get_authors(session: AsyncSession) -> list[Author]:
    result = await session.execute(select(Author))

    return result.scalars().all()


async def update_author(
    session: AsyncSession,
    author_id: int,
    author_update: AuthorUpdate
) -> Author:

    author = await session.get(Author, author_id)
    if not author:
        raise ValueError("Author not found")

    update_data = author_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(author, key, value)

    await session.commit()
    await session.refresh(author)

    return author


async def delete_author(session: AsyncSession, author_id: int) -> bool:
    author = await session.get(Author, author_id)
    if author:
        await session.delete(author)
        await session.commit()
        return True
    return False
