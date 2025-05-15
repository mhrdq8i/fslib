from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import get_session
from models.user import User
from schemas.user import UserCreate, UserRead, Token
from services.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.username == user.username)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    hashed = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(
        session,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password"
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
