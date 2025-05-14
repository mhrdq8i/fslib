from fastapi import Depends, APIRouter

from models.user import User
from dependencies import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/users/me")
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
