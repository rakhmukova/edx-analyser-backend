from celery import Celery

app = Celery('tasks')
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])