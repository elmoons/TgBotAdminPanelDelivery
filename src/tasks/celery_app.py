from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_instance = Celery(
    "tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks"]
)

celery_instance.conf.beat_schedule = {
    "name": {
        "task": "update_sheet_regularly",
        "schedule": 120,
        # crontab(day=3)
    }
}
