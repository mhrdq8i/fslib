from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserCreate, Token
from services.auth import authenticate_user, create_access_token
from services.user import create_user
from dependencies.auth import get_db, get_current_active_superuser

router = APIRouter(
    tags=["auth"]
)


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(
        session,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token}


@router.post("/users", response_model=UserCreate)
async def create_new_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    return await create_user(session, user_in)
