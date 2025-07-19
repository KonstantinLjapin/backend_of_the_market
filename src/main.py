from contextlib import asynccontextmanager
from src.middleware.cors import add_cors
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.avtoloader.routers import load_routers_from_package
from src.dependency.database import create_db_and_tables

description = """ MAXAZINE """

app = FastAPI(
    title="XXXXXX",
    description=description,
    summary="XXXXXXXX",
    version="0.0.1",
    contact={
        "name": "XXXXX",
        "telegram": "XXXXXX"
    }
)
origins = [
    "*",
]



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app.include_router(load_routers_from_package("src.routers"))
add_cors(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
