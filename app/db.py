from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import NullPool
from fastapi.testclient import TestClient
from httpx import AsyncClient

if settings.MODE == 'TEST':
    DATABASE_URL = str(settings.TEST_POSTGRES_DSN)
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


engine_nullpool = create_async_engine(DATABASE_URL, **DATABASE_PARAMS, echo=True)
async_session_maker_nullpool = async_sessionmaker(bind=engine_nullpool, class_=AsyncSession, expire_on_commit=False)

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Model(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
