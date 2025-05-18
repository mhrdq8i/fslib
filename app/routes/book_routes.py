from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.schemas.books import BookCreate, BookRead, BookUpdate
from app.services.book_service import BookService
from app.exceptions import NotFoundError


router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "/",
    response_model=List[BookRead]
)
async def list_books(
    session: AsyncSession = Depends(get_session)
):
    return await BookService(session).get_all()


@router.get(
    "/{book_id}",
    response_model=BookRead
)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await BookService(session).get_by_id(book_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED
)
async def create_book(
    data: BookCreate,
    session: AsyncSession = Depends(get_session)
):
    return await BookService(session).create(data)


@router.put(
    "/{book_id}",
    response_model=BookRead
)
async def update_book(
    book_id: int,
    data: BookUpdate,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await BookService(session).update(book_id, data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        await BookService(session).delete(book_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
    return None
