import smtplib
from datetime import date

import asyncio

from app.bookings.dao import BookingsDAO
from app.celery_config.celery_config import celery
from app.config import settings
from app.email_templates import remind_booking_reservation_template


@celery.task(name="periodic_task")
def periodic_task():
    return 1


@celery.task(name="reservation_reminder_one_day_before")
def reservation_reminder_one_day_before(days: int):
    date_from = date.today()
    bookings = asyncio.run(BookingsDAO.get_bookings_reservation_for_remind(date_from, days=days))
    with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:
        server.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
        for booking in bookings:
            msg_content = remind_booking_reservation_template(booking=booking.model_dump(), email_to=booking.user.email, days=days)
            server.send_message(msg=msg_content)


@celery.task(name="reservation_reminder_three_day_before")
def reservation_reminder_three_day_before(days: int):
    date_from = date.today()
    bookings = asyncio.run(BookingsDAO.get_bookings_reservation_for_remind(date_from, days=days))
    with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:
        server.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
        for booking in bookings:
            msg_content = remind_booking_reservation_template(booking=booking.model_dump(), email_to=booking.user.email, days=days)
            server.send_message(msg=msg_content)