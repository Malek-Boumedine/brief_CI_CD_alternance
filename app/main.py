import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routes import items_router

load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", True)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(items_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Items CRUD API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
