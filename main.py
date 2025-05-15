from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from sqlmodel import SQLModel

from routes import author_routes, auth_user
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(author_routes.router)
app.include_router(auth_user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
