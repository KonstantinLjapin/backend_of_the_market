from fastapi import APIRouter

from src.dependency.database import create_db_and_tables

base_router = APIRouter()


@base_router.get("/ping")
async def check():
    return {"ping": "pong!"}
