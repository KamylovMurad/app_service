from typing import Dict
from pydantic import EmailStr
from app.celery_config.celery_config import celery
from app.config import settings
from app.email_templates import create_booking_confirmation_template
import smtplib


@celery.task()
def send_booking_confirmation_email(
    booking: Dict,
    email_to: EmailStr,
):
    msg_content = create_booking_confirmation_template(booking, email_to)
    with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:
        server.login(user=settings.SMTP_USER, password=settings.SMTP_PASSWORD)
        server.send_message(msg=msg_content)
    return 1
