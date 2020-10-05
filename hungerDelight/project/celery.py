# from celery import Celery


# app = Celery('project', backend='rpc://',
#              broker='amqp://guest@localhost//',
#              include=['project.tasks', 'project.generateorder']
#              )

# if __name__ == '__main__':
#     app.start()
#     app.autodiscover_tasks()

from __future__ import absolute_import
import os


from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project', backend='rpc://',
             broker='amqp://guest@localhost//',
             include=['app.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
