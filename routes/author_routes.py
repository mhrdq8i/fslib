from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from schemas import AuthorCreate, AuthorRead
from services.author_service import AuthorService
from dependencies import get_current_user
from database import get_session


router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    dependencies=[Depends(get_current_user)],  # require auth on all endpoints
)


@router.get("/", response_model=List[AuthorRead])
async def list_authors(
    session: AsyncSession = Depends(get_session)
):
    return await AuthorService(session).get_all()


@router.get("/{author_id}", response_model=AuthorRead)
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


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_author(
    author_id: int,
    session: AsyncSession = Depends(get_session)
):
    await AuthorService(session).delete(author_id)
