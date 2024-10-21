from typing import Literal, Optional
from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

# DATABASE_URL = 'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'.format(
#     DB_USER=os.getenv('DB_USER'),
#     DB_PASS=os.getenv('DB_PASS'),
#     DB_HOST=os.getenv('DB_HOST'),
#     DB_PORT=os.getenv('DB_PORT'),
#     DB_NAME=os.getenv('DB_NAME')
# )


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str
    SENTRY_DSN: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: int
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DSN: Optional[PostgresDsn] = None

    @field_validator('TEST_POSTGRES_DSN')
    def validate_postgres_dsn(
        cls,
        field: PostgresDsn,
        fields: ValidationInfo,
    ) -> PostgresDsn:
        if field:
            return field
        return PostgresDsn(
            f'postgresql+asyncpg://{fields.data.get("TEST_POSTGRES_USER")}:'
            f'{fields.data.get("TEST_POSTGRES_PASSWORD")}@'
            f'{fields.data.get("TEST_POSTGRES_HOST")}:'
            f'{fields.data.get("TEST_POSTGRES_PORT")}/'
            f'{fields.data.get("TEST_POSTGRES_DB")}',
        )


    SECRET_KEY: str
    ALGORITHM: str

    REDIS_URL: str
    RABBIT_URL: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
