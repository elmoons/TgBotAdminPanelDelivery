from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    POIZON_API_KEY: str
    ADMIN_TG_IDS: str
    SPREADSHEET_URL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = "../.env"


settings = Settings()
