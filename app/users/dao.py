from app.dao_base.base import BaseDAO
from app.db import async_session_maker
from app.users.models import Users
from sqlalchemy import select


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_current_user(cls, **user_data):
        async with async_session_maker() as session:
            query = select(cls.model.id, cls.model.email, cls.model.name, cls.model.role).filter_by(**user_data)
            result = await session.execute(query)
            return result.mappings().one_or_none()
