from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_BROKER_DB: int
    REDIS_CACHE_DB: int

    USD_RATE_TTL: int
    CELERY_TASK_INTERVAL: int

    CBR_URL: str

    @property
    def database_url(self):
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    # "redis://localhost:6379/0"
    @property
    def broker_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_BROKER_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
