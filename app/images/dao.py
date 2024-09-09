from app.dao_base.base import BaseDAO
from app.rooms.models import ImageRooms


class ImageRoomsDAO(BaseDAO):
    model = ImageRooms

