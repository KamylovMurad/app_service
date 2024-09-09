from datetime import date
from sqlalchemy import ForeignKey, DECIMAL, Numeric, Computed
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db import Model
from app.rooms.models import Rooms
from app.users.models import Users


class Bookings(Model):
    __tablename__ = 'bookings'

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[DECIMAL] = mapped_column(Numeric(precision=10, scale=2))
    total_cost: Mapped[DECIMAL] = mapped_column(
        Numeric(precision=10, scale=2),
        Computed("(date_to - date_from) * price")
    )
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))
    user: Mapped["Users"] = relationship(back_populates='bookings')
    room: Mapped["Rooms"] = relationship(back_populates="bookings")

    def __str__(self):
        return f"Бронирование № {str(self.id)}"




# Модель написана в соответствии со старым стилем Алхимии (версии 1.x)
# class Bookings(Base):
#     __tablename__ = "bookings"

#     id = Column(Integer, primary_key=True)
#     room_id = Column(ForeignKey("rooms.id"))
#     user_id = Column(ForeignKey("users.id"))
#     date_from = Column(Date, nullable=False)
#     date_to = Column(Date, nullable=False)
#     price = Column(Integer, nullable=False)
#     total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
#     total_days = Column(Integer, Computed("date_to - date_from"))

#     user = relationship("Users", back_populates="booking")
#     room = relationship("Rooms", back_populates="booking")

#     def __str__(self):
#         return f"Booking #{self.id}"