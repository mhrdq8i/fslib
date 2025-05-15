from fastapi import HTTPException
from starlette import status


class EntityNotFoundException(HTTPException):
    def __init__(self, entity: str, entity_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} with ID {entity_id} not found"
        )


class EntityAlreadyExistsException(HTTPException):
    def __init__(self, entity_name: str):
        super().__init__(
            status_code=400,
            detail=f"{entity_name} already exists"
        )


class DatabaseIntegrityException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )


class AuthorHasBooksException(HTTPException):
    def __init__(self, author_id: int):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Author with ID {author_id} cannot be deleted - has associated books"
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Unauthorized"
        )


class ForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Forbidden"
        )
