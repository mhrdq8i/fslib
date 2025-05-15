from fastapi import APIRouter, Depends

from services.book import BookService
from dependencies.db_session import get_book_service
from schemas.book import BookCreate, BookRead, BookUpdate


router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "/",
    response_model=BookRead
)
async def create_book_route(
    *,
    service: BookService = Depends(get_book_service),
    book_in: BookCreate
):
    return await service.create_book(book_in)


@router.get(
    "/",
    response_model=list[BookRead]
)
async def get_all_books_route(
    *,
    service: BookService = Depends(get_book_service)
):
    return await service.get_all_books()


@router.get(
    "/{book_id}",
    response_model=BookRead
)
async def get_book_route(
    *,
    service: BookService = Depends(get_book_service),
    book_id: int
):
    return await service.get_book(book_id)


@router.put("/{book_id}", response_model=BookRead)
async def update_book_route(
    *,
    service: BookService = Depends(get_book_service),
    book_id: int,
    book_in: BookUpdate
):
    return await service.update_book(book_id, book_in)


@router.delete("/{book_id}", response_model=dict)
async def delete_book_route(
    *,
    service: BookService = Depends(get_book_service),
    book_id: int
):
    await service.delete_book(book_id)
    return {"status": "success"}
