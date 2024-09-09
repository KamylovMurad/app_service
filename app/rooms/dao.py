from sqlalchemy import select
from app.dao_base.base import BaseDAO
from app.db import async_session_maker
from app.rooms.models import Rooms
from sqlalchemy.orm import selectinload, joinedload

from app.rooms.schemas import RoomsSchema


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def test_all(cls, **filter_by):
        """Данный вариант с model.__table__.columns предпочтительнее,
        т к берет не 1 значение из кортежа, а переводит все в словарь,
        удобно если мы получаем значение типа так: Rooms.id, Rooms.price, Hotels и тд."""
        async with async_session_maker() as session:
            # query = select(cls.model.__table__.columns, cls.model.id).filter_by(**filter_by)
            # query = select(cls.model.__table__.columns, cls.model.hotel).options(selectinload(cls.model.hotel)).filter_by(**filter_by)
            query = select(cls.model).options(selectinload(cls.model.hotel)).filter_by(**filter_by)
            result = await session.execute(query)
            # return result.mappings().all()
            return result.scalars().all()

    @classmethod
    async def get_one_room(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.hotel)).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_room_with_images(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.images)).options(joinedload(cls.model.hotel)).filter_by(**filter_by)
            result = await session.execute(query)
            # return await session.scalars(query)
            return result.scalars().unique().all()
            # return result.mappings().unique().all()