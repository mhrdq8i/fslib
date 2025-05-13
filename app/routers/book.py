# routers/book.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from schemas.book import BookCreate, BookRead, BookUpdate
from services.book import (
    create_book, get_books, update_book, delete_book, get_book_by_id
)
from core.database import get_session


router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookRead)
async def create_book_route(
    *,
    session: AsyncSession = Depends(get_session),
    book_in: BookCreate
):
    return await create_book(session, book_in)


@router.get("/", response_model=Annotated[List[BookRead], ...])
async def get_books_route(
    *,
    session: AsyncSession = Depends(get_session)
):
    books = await get_books(session)

    # Force relationship loading while session is active
    for book in books:
        await session.refresh(book, attribute_names=["author"])

    return books


@router.get("/{book_id}", response_model=BookRead)
async def get_book_route(
    *,
    session: AsyncSession = Depends(get_session),
    book_id: int
):
    return await get_book_by_id(session, book_id)


@router.put("/{book_id}", response_model=BookRead)
async def update_book_route(
    *,
    session: AsyncSession = Depends(get_session),
    book_id: int,
    book_in: BookUpdate
):
    book = await update_book(session, book_id, book_in)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", response_model=dict)
async def delete_book_route(
    *,
    session: AsyncSession = Depends(get_session),
    book_id: int
):
    success = await delete_book(session, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "success"}
