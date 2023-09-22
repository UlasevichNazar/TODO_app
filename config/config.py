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

    EMAIL: str
    PASSWORD: str

    DATABASE_URL: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


setting = Setting()
