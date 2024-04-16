from typing import TYPE_CHECKING
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Model


# from app.rooms.models import Rooms

# if TYPE_CHECKING:
#     # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в
#     # PyCharm и VSCode
#     from app.rooms.models import Rooms

class Hotels(Model):
    __tablename__ = 'hotels'

    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]
    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

# Модель написана в соответствии со старым стилем Алхимии (версии 1.x)
# class Hotels(Base):
#     __tablename__ = "hotels"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     location = Column(String, nullable=False)
#     services = Column(JSON)
#     rooms_quantity = Column(Integer, nullable=False)
#     image_id = Column(Integer)

#     rooms = relationship("Rooms", back_populates="hotel")

#     def __str__(self):
#         return f"Отель {self.name} {self.location[:30]}"
