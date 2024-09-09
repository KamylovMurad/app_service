from email.message import EmailMessage
from typing import Dict

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
        booking: Dict,
        email_to: EmailStr,
):
    email = EmailMessage()
    email['Subject'] = 'Подтверждение бронирования'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
               <h1> Подтвердите бронирование</h1>
                Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
                """,
        subtype='html',
    )
    return email


def remind_booking_reservation_template(
    booking: Dict,
    email_to: EmailStr,
    days: int
):
    email = EmailMessage()
    email['Subject'] = f'Осталось {days} дня до заселения'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
               <h1> Напоминание о бронировании</h1>
                Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
                """,
        subtype='html',
    )
    return email
