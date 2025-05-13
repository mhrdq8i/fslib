from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from core.database import engine
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
async def root():
    return {"message": "Async Library Service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
