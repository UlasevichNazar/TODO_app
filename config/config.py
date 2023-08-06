from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    FASTAPI_HOST: str
    FASTAPI_PORT: str

    POSTGRES_ENGINE: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


setting = Setting()
