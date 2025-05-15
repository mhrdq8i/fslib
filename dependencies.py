from jwt import PyJWTError, encode, decode
from datetime import datetime, timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from config import settings
from exceptions import credentials_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # decode returns the payload as a dict
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"require": ["exp", "sub"]},
        )
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    return {"username": username}


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    expire = datetime.utcnow() + \
        (expires_delta or timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
         )
    to_encode.update({"exp": expire})

    return encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
