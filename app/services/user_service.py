from passlib.context import CryptContext

from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import User
from app.schemas.users import UserCreate, UserUpdate
from app.exceptions import ConflictError, NotFoundError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    async def create_user(self, user_in: UserCreate) -> User:
        # Check existing
        q = await self.session.exec(
            select(User).where(
                User.username == user_in.username
            )
        )

        if q.first():
            raise ConflictError("Username already taken")

        user = User(
            username=user_in.username,
            hashed_password=self._hash(user_in.password),
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def authenticate(
            self,
            username: str,
            password: str
    ) -> User:
        q = await self.session.exec(
            select(User).where(
                User.username == username
            )
        )
        user = q.first()
        if not user or not self.verify(password, user.hashed_password):
            raise NotFoundError("Incorrect username or password")

        return user

    async def get_all_users(self) -> list[User]:
        result = await self.session.exec(select(User))

        return result.all()

    async def get_user_by_id(self, user_id: int):
        result = await self.session.get(User, user_id)
        return result

    async def update_user(
        self,
        user_id: int,
        data: UserUpdate
    ) -> User | None:

        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(user, k, v)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)

        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()

        return True
