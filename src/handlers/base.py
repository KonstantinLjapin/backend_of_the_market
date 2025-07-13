from fastapi import APIRouter

base_router = APIRouter()


@base_router.get("/ping")
async def check():
    return {"ping": "pong!"}
