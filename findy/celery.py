import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'findy.settings')

app = Celery('findy')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()