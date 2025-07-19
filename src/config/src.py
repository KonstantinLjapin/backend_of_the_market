from pydantic_settings import BaseSettings
from typing import Optional


class AppSettings(BaseSettings):
    title: str = "XXXXXX"
    description: str = "MAXAZINE"
    summary: str = "XXXXXXXX"
    version: str = "0.0.1"
    contact_name: Optional[str] = "XXXXX"
    contact_telegram: Optional[str] = "XXXXXX"


    class Config:
        env_file = "../.env"
        env_prefix = "APP_"
