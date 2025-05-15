
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from schemas import Token
from services.user_service import UserService
from database import get_session
from dependencies import create_access_token


router = APIRouter()


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
