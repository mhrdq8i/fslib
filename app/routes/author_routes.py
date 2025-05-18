from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dependencies import get_current_user
from app.core.database import get_session
from app.schemas.authors import AuthorCreate, AuthorRead, AuthorUpdate
from app.services.author_service import AuthorService


router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/",
    response_model=List[AuthorRead]
)
async def list_authors(
    session: AsyncSession = Depends(get_session)
):
    return await AuthorService(session).get_all()


@router.get(
    "/{author_id}",
    response_model=AuthorRead
)
async def get_author(
    author_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await AuthorService(session).get_by_id(author_id)


@router.post(
    "/",
    response_model=AuthorRead,
    status_code=status.HTTP_201_CREATED
)
async def create_author(
    author_in: AuthorCreate,
    session: AsyncSession = Depends(get_session)
):
    return await AuthorService(session).create(author_in)


@router.put(
    "/{author_id}",
    response_model=AuthorRead
)
async def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await AuthorService(session).update(author_id, author_in)


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_author(
    author_id: int,
    session: AsyncSession = Depends(get_session)
):
    await AuthorService(session).delete(author_id)
