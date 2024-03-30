import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
# move to env

app = Celery('tasks')
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])