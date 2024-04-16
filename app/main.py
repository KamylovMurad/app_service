from fastapi import FastAPI
from app.bookings.router import router as router_booking
from app.hotels.router import router as router_hotels
from app.rooms.router import router as router_rooms
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_booking)
app.include_router(router_hotels)
app.include_router(router_rooms)

