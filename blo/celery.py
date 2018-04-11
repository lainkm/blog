from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blo.settings')
 
app = Celery('blo')
 
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')
 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
 
 
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))