
from typing import List

from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from schemas import Token, UserRead, UserCreate, UserUpdate
from services.user_service import UserService
from database import get_session
from dependencies import (
    create_access_token,
    get_current_active_superuser
)


router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Create a new user account (sign‑up).
    """
    user = await UserService(session).create_user(user_in)

    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await UserService(session).authenticate(
        form_data.username,
        form_data.password
    )
    access_token = create_access_token({"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/",
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_superuser)],
)
async def list_users(
    session: AsyncSession = Depends(get_session),

):
    """
    Return all registered users.
    Protected: requires a valid Bearer token.
    """
    users = await UserService(session).get_all_users()

    return users


@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_active_superuser)],
)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    user = await UserService(session).get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_active_superuser)]
)
async def update_user(
        user_id: int,
        data: UserUpdate,
        session: AsyncSession = Depends(get_session)
):
    user = await UserService(session).update_user(user_id, data)

    if not user:
        raise HTTPException("User not found")

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_superuser)],
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    success = await UserService(session).delete_user(user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return None
