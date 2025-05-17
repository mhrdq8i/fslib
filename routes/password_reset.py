from datetime import timedelta
from passlib.context import CryptContext

from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from jwt import decode
from jwt.exceptions import PyJWTError

from config import settings
from dependencies import create_access_token
from database import get_session
from models import User
from schemas import PasswordResetRequest, PasswordResetConfirm
from exceptions import BadRequestError, NotFoundError


router = APIRouter(tags=["password-reset"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    "/password-reset/request",
    status_code=status.HTTP_202_ACCEPTED,
)
async def password_reset_request(
    data: PasswordResetRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    1. Lookup user by email (username).
    2. If found, create a short‑lived JWT with type="pw-reset".
    3. Return it in the response for testing.
    """
    # 1. Lookup
    result = await session.exec(
        select(User).where(
            User.username == data.email
        )
    )
    user = result.one_or_none()

    # 2. Generate token if user exists
    reset_token: str | None = None
    if user:
        expires = timedelta(minutes=15)
        reset_token = create_access_token(
            data={"sub": user.username, "type": "pw-reset"},
            expires_delta=expires,
        )

    # 3. Always 202, never leak existence
    return {
        "msg": "If that account exists, you’ll receive a reset token.",
        "reset_token": reset_token,
    }


@router.post("/password-reset/confirm")
async def password_reset_confirm(
    data: PasswordResetConfirm,
    session: AsyncSession = Depends(get_session),
):
    """
    1. Decode & verify JWT (signature, exp).
    2. Check payload["type"] == "pw-reset".
    3. Lookup user by payload["sub"].
    4. Hash new_password & update user.
    """
    # 1. Decode token
    try:
        payload = decode(
            data.token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"require": ["exp", "sub"]},
        )
    except PyJWTError:
        raise BadRequestError("Invalid or expired token")

    # 2. Validate token type
    if payload.get("type") != "pw-reset":
        raise BadRequestError("Invalid token type")

    username = payload.get("sub")
    if not username:
        raise BadRequestError("Invalid token payload")

    # 3. Lookup user
    result = await session.exec(
        select(User).where(
            User.username == username
        )
    )
    user = result.one_or_none()
    if not user:
        raise NotFoundError("User not found")

    # 4. Update password
    user.hashed_password = pwd_context.hash(data.new_password)
    session.add(user)
    await session.commit()

    return {"msg": "Password has been reset successfully"}
