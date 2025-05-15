from fastapi import APIRouter, Depends

from models.user import User
from services.book import BookService
from schemas.book import BookCreate, BookRead
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get("/books", response_model=list[BookRead])
async def list_books(
    book_service: BookService = Depends(BookService.get_book())
):
    return await book_service.list_books()


@router.get("/books/{book_id}", response_model=BookRead)
async def get_book(
    book_id: int,
    book_service: BookService = Depends(BookService.get_book())
):
    return await book_service.get_book(book_id)


@router.post("/books", response_model=BookRead)
async def create_new_book(
    book_in: BookCreate,
    book_service: BookService = Depends(BookService.get_book()),
    current_user: User = Depends(get_current_user)
):
    return await book_service.create_book(book_in)
