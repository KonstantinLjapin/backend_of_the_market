from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def check():
    return {"ping": "pong!"}
