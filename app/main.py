from contextlib import asynccontextmanager
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import (
    BookingsAdmin,
    HotelsAdmin,
    ImageRoomsAdmin,
    RoomsAdmin,
    UserAdmin,
)

from app.bookings.router import router as router_booking
from app.config import settings
from app.db import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.rooms.router import router as router_rooms
from app.users.router import router as router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(url=settings.REDIS_URL)
    FastAPICache.init(backend=RedisBackend(redis), prefix="cache")
    logger.info("Service started")
    yield
    logger.info("Service exited")

app = FastAPI(lifespan=lifespan)

app.mount(
    path="/static",
    app=StaticFiles(directory="app/static"),
    name="static",
)

admin = Admin(app, engine, authentication_backend=authentication_backend)

app.include_router(router_users)
app.include_router(router_booking)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)

# "Устаревший вариант подключения кеширования, т к предпочтительннее lifespan, а от on_event хотят отказаться
# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url(url=settings.REDIS_URL)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")


# @app.on_event("shutdown")  # <-- данный декоратор прогоняет код после завершения программы
# def shutdown_event():
#     logger.info("Service exited")

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(ImageRoomsAdmin)
