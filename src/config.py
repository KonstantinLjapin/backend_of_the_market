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


class SettingsAuthorization(BaseSettings):
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    secret_key: str

    class Config:
        env_file = "../.env"
        extra = "allow"


class SettingsBaseAdmin(BaseSettings):
    market_admin_email: str
    market_admin_password: str

    class Config:
        env_file = "../.env"
        extra = "allow"


admin_settings: SettingsBaseAdmin = SettingsBaseAdmin()
settings_authorization: SettingsAuthorization = SettingsAuthorization()
db_settings: SettingsDataBase = SettingsDataBase()

