from celery import Celery

import os
os.environ.setdefault('"DJANGO_SETTINGS_MODULE", "E_business_project.settings.dev"')

app = Celery('celery_tasks')

app.autodiscover_tasks(['celery_tasks.sms'])