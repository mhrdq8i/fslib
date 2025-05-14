from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from dependencies import oauth2_scheme, authenticate_user, get_user
from schemas.user import Token
from models.user import User

router = APIRouter(
    tags=["user"]
)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Simple token creation (replace with JWT implementation)
    access_token = f"fake-jwt-token-{user.username}"
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token.startswith("fake-jwt-token-"):
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")
    username = token.replace("fake-jwt-token-", "")
    user = await get_user(username)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")
    return user


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}
