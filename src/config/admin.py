from pydantic_settings import BaseSettings

class SettingsBaseAdmin(BaseSettings):
    market_admin_email: str
    market_admin_password: str

    class Config:
        env_file = "../.env"
        extra = "allow"

admin_settings = SettingsBaseAdmin()
