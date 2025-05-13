from fastapi import APIRouter, Depends

from services.book import BookService
from dependencies import get_book_service
from schemas.book import BookCreate, BookRead


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


@router.get(
    "/author/{author_id}",
    response_model=list[BookRead]
)
async def get_books_by_author_route(
    *,
    service: BookService = Depends(get_book_service),
    author_id: int
):
    return await service.get_books_by_author(author_id)
