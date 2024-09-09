from datetime import date
from sqlalchemy import select, func, or_, update

from app.bookings.models import Bookings
from app.dao_base.base import BaseDAO
from app.db import async_session_maker
from app.hotels.models import Hotels
from app.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_rooms_by_hotel(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            total_days = date_to - date_from
            booked_dates = select(Bookings).filter(
                Bookings.date_from <= date_from,
                Bookings.date_to >= date_to
            ).cte("booked_dates")

            get_left_rooms = select(
                Rooms.__table__.columns,
                (Rooms.price * int(total_days.days)).label('total_cost'),
                (Rooms.quantity_rooms - func.count(booked_dates.c.room_id)).label('free_rooms'),
            ).filter_by(hotel_id=hotel_id).join(
                booked_dates, booked_dates.c.room_id == Rooms.id, isouter=True
            ).group_by(Rooms.id).order_by(Rooms.id)

            rooms = await session.execute(get_left_rooms)
            return rooms.mappings().all()

    @classmethod
    async def get_hotel_by_city(
            cls,
            location: str,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            booked_dates = select(
                Bookings.room_id,
                func.count(Bookings.room_id).label('books_count'),
            ).filter(
                Bookings.date_from <= date_from,
                Bookings.date_to >= date_to
            ).group_by(Bookings.room_id).cte('booked_dates')

            booked_rooms = select(
                Rooms.__table__.columns,
                func.coalesce(booked_dates.c.books_count, 0).label('books_count'),
                (Rooms.quantity_rooms - func.coalesce(booked_dates.c.books_count, 0)).label('free_rooms')
            ).join(
                booked_dates, booked_dates.c.room_id == Rooms.id, isouter=True
            ).filter(
                or_(Rooms.quantity_rooms - booked_dates.c.books_count > 0,
                    booked_dates.c.books_count.is_(None))).order_by(Rooms.hotel_id).cte('booked_rooms')

            left_hotels = select(
                Hotels.__table__.columns,
                # func.sum(booked_rooms.c.quantity_rooms).label('count'),
                func.sum(booked_rooms.c.free_rooms).label('free_rooms')
            ).join(
                booked_rooms, booked_rooms.c.hotel_id == Hotels.id
            ).group_by(Hotels.id).order_by(Hotels.id).filter(Hotels.location.like(f'%{location}%'))

            result = await session.execute(left_hotels)
            return result.mappings().all()

# 1 : 10
# 2: 23
# 3 : 30
# 4: 53
# 5: 22
# 6: 45

    @classmethod
    async def update_image_id(cls, hotel: Hotels, image_id: int):
        async with async_session_maker() as session:
            query = update(Hotels).filter_by(id=hotel.id).values(image_id=image_id)
            await session.execute(query)
            await session.commit()