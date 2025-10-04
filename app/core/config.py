from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CatalogFlow"
    PROJECT_VERSION: str = "0.1.0"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
