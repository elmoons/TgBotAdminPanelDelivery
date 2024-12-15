from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    POIZON_API_KEY: str
    ADMIN_TG_IDS: str
    SPREADSHEET_URL: str

    class Config:
        env_file = "../.env"


settings = Settings()
