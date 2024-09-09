from typing import Optional, TYPE_CHECKING, List
from sqlalchemy import JSON, ForeignKey, DECIMAL, Numeric, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Model
from app.hotels.models import Hotels


if TYPE_CHECKING:
    from bookings.models import Bookings
    from hotels.models import Hotels


class Rooms(Model):
    __tablename__ = 'rooms'

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(VARCHAR(length=150))
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[DECIMAL] = mapped_column(Numeric(precision=10, scale=2))
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    quantity_rooms: Mapped[int]
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    images: Mapped[List["ImageRooms"]] = relationship(back_populates="room")
    bookings: Mapped[List["Bookings"]] = relationship(back_populates="room")

    def __str__(self):
        return f'Номер: {self.name}'


class ImageRooms(Model):
    __tablename__ = 'images'

    name: Mapped[str]
    path: Mapped[Optional[str | None]]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Rooms"] = relationship(back_populates="images")

    def __str__(self):
        return f'{self.name}'


# Модель написана в соответствии со старым стилем Алхимии (версии 1.x)
# class Rooms(Base):
#     __tablename__ = "rooms"

#     id = Column(Integer, primary_key=True)
#     hotel_id = Column(ForeignKey("hotels.id"), )
#     name = Column(String, )
#     description = Column(String, nullable=True)
#     price = Column(Integer, )
#     services = Column(JSON, nullable=True)
#     quantity = Column(Integer, )
# image_id = Column(Integer)

#     hotel = relationship("Hotels", back_populates="rooms")
#     booking = relationship("Bookings", back_populates="room")

#     def __str__(self):
#         return f"Номер {self.name}"
