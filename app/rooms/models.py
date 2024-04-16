from typing import Optional, TYPE_CHECKING
from sqlalchemy import JSON, ForeignKey, DECIMAL, Numeric, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Model
from app.hotels.models import Hotels


# if TYPE_CHECKING:
#     # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в
#     # PyCharm и VSCode
#     from app.hotels.models import Hotels


class Rooms(Model):
    __tablename__ = 'rooms'

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(VARCHAR(length=150))
    description: Mapped[str]
    price: Mapped[DECIMAL] = mapped_column(Numeric(precision=10, scale=2))
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    quantity_rooms: Mapped[int]
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    #hotel = relationship("Hotels", back_populates="rooms")


class ImageRooms(Model):
    __tablename__ = 'images'

    name: Mapped[str]
    path: Mapped[Optional[str | None]]
    room: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    def save_image(self, image_data):
        file_name = f"{self.id}_{self.name}.jpg"
        file_path = f'app/images/{self.room}/{file_name}'
        with open(file_path, 'wb') as file:
            file.write(image_data)

        self.path = file_path

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
