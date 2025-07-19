from pydantic_settings import BaseSettings
from typing import List

class CorsSettings(BaseSettings):
    allow_origins: List[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]
    expose_headers: List[str] = ["Content-Disposition"]

    class Config:
        env_file = "../.env"
        env_prefix = "CORS_"
