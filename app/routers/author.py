from fastapi import APIRouter, Depends

from services.author import AuthorService
from schemas.author import AuthorCreate, AuthorRead, AuthorUpdate
from schemas.book import BookRead
from dependencies import get_author_service


router = APIRouter(prefix="/authors", tags=["authors"])


@router.get(
    "/",
    response_model=list[AuthorRead]
)
async def get_all_authors_route(
    *,
    service: AuthorService = Depends(get_author_service)
):
    return await service.get_all_authors()


@router.post(
    "/",
    response_model=AuthorRead
)
async def create_author_route(
    *,
    service: AuthorService = Depends(get_author_service),
    author_in: AuthorCreate
):
    return await service.create_author(author_in)


@router.get(
    "/{author_id}",
    response_model=AuthorRead
)
async def get_author_route(
    *,
    service: AuthorService = Depends(get_author_service),
    author_id: int
):
    return await service.get_author(author_id)


@router.put(
    "/{author_id}",
    response_model=AuthorRead
)
async def update_author_route(
    *,
    service: AuthorService = Depends(get_author_service),
    author_id: int,
    author_in: AuthorUpdate
):
    return await service.update_author(author_id, author_in)


@router.delete(
    "/{author_id}",
    response_model=dict
)
async def delete_author_route(
    *,
    service: AuthorService = Depends(get_author_service),
    author_id: int
):
    await service.delete_author(author_id)
    return {"status": "success"}


@router.get(
    "/{author_id}/books",
    response_model=list[BookRead]
)
async def get_books_by_author_route(
    *,
    service: AuthorService = Depends(get_author_service),
    author_id: int
):
    return await service.get_books_by_author(author_id)
