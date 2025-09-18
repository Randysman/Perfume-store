import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')


app = Celery('shop.celery', broker=os.getenv('CELERY_BROKER_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()