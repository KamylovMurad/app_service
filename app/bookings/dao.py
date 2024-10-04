from datetime import date, timedelta
from typing import List

from sqlalchemy import select, func, insert, delete
from sqlalchemy.orm import selectinload

from app.bookings.models import Bookings
from app.bookings.schemas import SchemaEmailBooking
from app.dao_base.base import BaseDAO
from app.db import async_session_maker, async_session_maker_nullpool
from app.rooms.models import Rooms


class BookingsDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).filter(
                Bookings.room_id == room_id,
                Bookings.date_from <= date_from,
                Bookings.date_to >= date_to
                # or_(
                #     and_(
                #         Bookings.date_from >= date_from,
                #         Bookings.date_from <= date_to,
                #     ),
                #     and_(
                #         Bookings.date_from <= date_from,
                #         Bookings.date_to > date_from,
                #     ),
                # ),
            ).cte("booked_rooms")

            left_rooms = select(
                Rooms.quantity_rooms - func.count(booked_rooms.c.room_id).label("left_rooms")
            ).select_from(Rooms).filter_by(id=room_id).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).group_by(Rooms.quantity_rooms, booked_rooms.c.room_id)
            # ).group_by(Rooms.id)

            result = await session.execute(left_rooms)
            rooms_left = result.scalar()
            print(rooms_left)
            if rooms_left > 0:
                # get_price = select(Rooms.price).filter_by(id=room_id) #Данный вариант более верный
                get_price = select(Rooms).filter(Rooms.id == room_id)
                price = await session.execute(get_price)
                price = price.scalar()
                price = price.price

                "Первый способ добавления новой модели синхр."
                # new_booking = Bookings(
                #     price=price,
                #     room_id=room_id,
                #     user_id=user_id,
                #     date_to=date_to,
                #     date_from=date_from
                # )
                # session.add(new_booking)
                new_booking = insert(Bookings).values(
                    price=price,
                    room_id=room_id,
                    user_id=user_id,
                    date_to=date_to,
                    date_from=date_from
                ).returning(Bookings)
                new_booking = await session.execute(new_booking)
                await session.commit()
                return new_booking.scalar()
            return

    @classmethod
    async def get_bookings(cls, user_id: int):
        user_bookings = select(
            Bookings.__table__.columns,
            Rooms.name,
            Rooms.description,
            Rooms.services
        ).filter_by(user_id=user_id).join(Rooms, Rooms.id == Bookings.room_id)
        async with async_session_maker() as session:
            result = await session.execute(user_bookings)
            return result.mappings().all()

    @classmethod
    async def delete_booking(cls, booking_id: int, user_id: int):
        query = delete(cls.model).filter_by(id=booking_id, user_id=user_id).returning(cls.model.id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def test_func(
        cls,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        booked_rooms = select(Bookings).filter(
            Bookings.room_id == room_id,
            Bookings.date_from <= date_from,
            Bookings.date_to >= date_to)
        async with async_session_maker() as session:
            result = await session.execute(booked_rooms)
            return result.scalars().all()

    @classmethod
    async def get_bookings_reservation_for_remind(cls, date_now: date, days: int = 1) -> List[SchemaEmailBooking]:
        next_day = date_now + timedelta(days=days)
        async with async_session_maker_nullpool() as session:
            bookings_user_mails = await session.scalars(select(cls.model).options(
                selectinload(cls.model.user),
            ).filter(cls.model.date_from == next_day))
            return [SchemaEmailBooking.model_validate(booking, from_attributes=True) for booking in
                    bookings_user_mails.all()]
