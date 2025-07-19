from pydantic_settings import BaseSettings

class SettingsDataBase(BaseSettings):
    postgres_host: str
    postgres_user: str
    postgres_db: str
    postgres_port: str
    postgres_password: str
    db_container_name: str

    class Config:
        env_file = "../.env"
        extra = "allow"

db_settings = SettingsDataBase()
