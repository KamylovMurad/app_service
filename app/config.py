from pydantic_settings import BaseSettings, SettingsConfigDict

# DATABASE_URL = 'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'.format(
#     DB_USER=os.getenv('DB_USER'),
#     DB_PASS=os.getenv('DB_PASS'),
#     DB_HOST=os.getenv('DB_HOST'),
#     DB_PORT=os.getenv('DB_PORT'),
#     DB_NAME=os.getenv('DB_NAME')
# )


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
