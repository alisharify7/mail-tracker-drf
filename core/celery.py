import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.enable_utc = True
app.conf.timezone = 'UTC'
# Load task modules from all registered Django apps.
app.autodiscover_tasks()
# https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html
