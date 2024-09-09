from celery import Celery
from app.config import settings
from celery.schedules import crontab


celery = Celery(
    'app',
    broker=settings.RABBIT_URL,
    backend='rpc://',
    include=[
        "app.bookings.tasks",
        "app.celery_config.scheduled",
    ]
)

celery.conf.beat_schedule = {
    # "some": {
    #     "task": "periodic_task",
    #     "schedule": 5
    #     # "schedule": crontab(hour="15", minute="30")
    # },
    "reservation_reminder_one_day_before": {
        "task": "reservation_reminder_one_day_before",
        "schedule": crontab(hour="9"),
        "kwargs": {"days": 1}
    },
    "reservation_reminder_three_day_before": {
        "task": "reservation_reminder_three_day_before",
        "schedule": crontab(hour="15", minute="30"),
        "kwargs": {"days": 3},
    }
}
