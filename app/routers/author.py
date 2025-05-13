# routers/author.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from schemas.book import BookRead
from services.book import get_books_by_author
from schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from services.author import (
    create_author, get_authors, update_author,
    delete_author, get_author_by_id
)

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/", response_model=AuthorRead)
async def create_author_route(
    *,
    session: AsyncSession = Depends(get_session),
    author_in: AuthorCreate
):
    return await create_author(session, author_in)


@router.get("/", response_model=List[AuthorRead])
async def get_authors_route(
    *,
    session: AsyncSession = Depends(get_session)
):
    return await get_authors(session)


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author_route(
    *,
    session: AsyncSession = Depends(get_session),
    author_id: int
):
    return await get_author_by_id(session, author_id)


@router.put("/{author_id}", response_model=AuthorRead)
async def update_author_route(
    *,
    session: AsyncSession = Depends(get_session),
    author_id: int,
    author_in: AuthorUpdate
):
    author = await update_author(session, author_id, author_in)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.get("/{author_id}/books", response_model=list[BookRead])
async def get_author_books_route(
    *,
    session: AsyncSession = Depends(get_session),
    author_id: int
):
    return await get_books_by_author(session, author_id)


@router.delete("/{author_id}", response_model=dict)
async def delete_author_route(
    *,
    session: AsyncSession = Depends(get_session),
    author_id: int
):
    success = await delete_author(session, author_id)
    if not success:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"status": "success"}
