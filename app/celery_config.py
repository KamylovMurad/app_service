from celery import Celery

appi = Celery(
    'app',
    broker='pyamqp://guest:guest@localhost//',
    backend='rpc://',
    include=[
        "tasks",
        # "app.tasks.scheduled",
    ]
)
