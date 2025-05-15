from contextlib import asynccontextmanager

from uvicorn import run as run_server
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel

from core.database import engine
from dependencies.db_session import oauth2_scheme
from routers import author, book


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(title="fslib", lifespan=lifespan)

app.include_router(router=author.router)
app.include_router(router=book.router)


@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
    return {"token": token}


if __name__ == "__main__":
    run_server(
        app=app,
        host="0.0.0.0",
        port=8000
    )
