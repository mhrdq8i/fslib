# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from core.database import engine
from routers.author import router as author_router
from routers.book import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(title="minimal_async", lifespan=lifespan)
app.include_router(author_router)
app.include_router(book_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
