from celery import Celery
from app.core.config import settings

celery_app = Celery("application_platform", broker=settings.redis_url)

