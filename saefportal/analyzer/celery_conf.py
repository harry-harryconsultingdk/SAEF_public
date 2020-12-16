""" create celery instance """
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saefportal.settings')

app = Celery('analyzer',
             broker='pyamqp://guest@localhost//',
             backend='amqp://',
             include=['analyzer.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
