from fastapi import APIRouter
from src.dependency.database import create_db_and_tables
base_router = APIRouter()


@base_router.get("/ping")
async def check():
    return {"ping": "pong!"}


"""@base_router.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()"""
