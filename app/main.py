from contextlib import asynccontextmanager

from uvicorn import run as run_server
from sqlalchemy import select
from sqlmodel import SQLModel
from fastapi import FastAPI

from models.user import User
from routers import author, book, auth
from services.user import create_user
from core.database import engine, init_db
from dependencies.auth import get_db
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(title="fslib", lifespan=lifespan)

app.include_router(router=author.router)
app.include_router(router=book.router)
app.include_router(router=auth.router)


# @app.get("/")
# async def root(token: str = Depends(oauth2_scheme)):
#     return {"token": token}


@app.on_event("startup")
async def startup_event():
    await init_db()
    async with get_db() as session:
        # Create super admin if no users exist
        result = await session.execute(select(User))
        if not result.scalars().all():
            await create_user(
                session,
                User(
                    username=settings.SUPER_ADMIN_USERNAME,
                    password=settings.SUPER_ADMIN_PASSWORD,
                    is_superuser=True
                )
            )


if __name__ == "__main__":
    run_server(
        app=app,
        host="0.0.0.0",
        port=8000
    )
