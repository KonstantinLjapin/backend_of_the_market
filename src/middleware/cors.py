from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.config.cors import CorsSettings

def add_cors(app: FastAPI) -> None:
    settings = CorsSettings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,          # здесь list[str] не забываем что через запятую))
        allow_credentials=settings.allow_credentials,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
        expose_headers=settings.expose_headers,
    )

