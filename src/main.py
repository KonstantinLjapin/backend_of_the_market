import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from dependency.database import DatabaseHelper

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


if __name__ == "__main__":
    # запуск сервера
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
