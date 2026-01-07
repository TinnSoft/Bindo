import os
from celery import Celery

REDIS = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
celery = Celery('bindo', broker=REDIS, backend=REDIS)

celery.conf.task_routes = {
    'app.tasks.*': {'queue': 'default'}
}
celery.conf.include = ['app.tasks']
