from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import engine
from app.db.models import Base
from app.api.routes.todos import router as todos_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Todo API", lifespan=lifespan)

app.include_router(todos_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Todo API"}
