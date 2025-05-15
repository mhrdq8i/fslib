from fastapi import APIRouter, Depends

from models.user import User
from services.author import AuthorService
from schemas.author import AuthorCreate, AuthorRead

router = APIRouter(tags=["authors"])


@router.get("/authors", response_model=list[AuthorRead])
async def list_authors(author_service: AuthorService = Depends(AuthorService.get_author())):
    return await author_service.list_authors()


@router.get("/authors/{author_id}", response_model=AuthorRead)
async def get_author(
    author_id: int,
    author_service: AuthorService = Depends(AuthorService.get_author())
):
    return await author_service.get_author(author_id)


@router.post("/authors", response_model=AuthorRead)
async def create_new_author(
    author_in: AuthorCreate,
    author_service: AuthorService = Depends(AuthorService.get_author()),
    current_user: User = Depends(AuthorService.get_author())
):
    return await author_service.create_author(author_in)
