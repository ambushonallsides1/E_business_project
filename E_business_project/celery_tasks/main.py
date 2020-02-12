from celery import Celery

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "E_business_project.settings.dev")

app = Celery('E_business_project')

#3.加载配置文件
app.config_from_object('celery_tasks.config')

app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email','celery_tasks.html'])