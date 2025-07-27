from pydantic_settings import BaseSettings

class SettingsAuthorization(BaseSettings):
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    secret_key: str

    class Config:
        env_file = "../.env"
        env_prefix= "AUTH_"
        extra = "allow"

settings_authorization = SettingsAuthorization()
