from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from time import monotonic
import logging
import functools
from django.core.cache import cache

# Get an instance of a logger
logger = logging.getLogger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mm_tools.web.settings')

app = Celery('mm_tools.web')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

CACHE_LOCK_EXPIRE = 30


def no_simultaneous_execution(retry=60*5, expires=60*30):
    def wrap(f):
        """
        Decorator that prevents a task form being executed with the
        same *args and **kwargs more than one at a time. It will attempt a retry,
        if the retry fails it will not retry the retry.
        """
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            # Create lock_id used as cache key
            lock_id = '{}-{}-{}'.format(self.name, args, kwargs)

            # Timeout with a small diff, so we'll leave the lock delete
            # to the cache if it's close to being auto-removed/expired
            timeout_at = monotonic() + CACHE_LOCK_EXPIRE - 3

            # Try to acquire a lock, or put task back on queue
            lock_acquired = cache.add(lock_id, True, CACHE_LOCK_EXPIRE)

            _retry = kwargs.pop('_retry', False)
            if not lock_acquired:
                if _retry:
                    return
                kwargs['_retry'] = True

                self.apply_async(args=args, kwargs=kwargs,
                                 countdown=retry, expires=expires)
                return

            try:
                f(self, *args, **kwargs)
            finally:
                # Release the lock
                if monotonic() < timeout_at:
                    cache.delete(lock_id)
        return wrapper
    return wrap


@app.task(bind=True, name='mm_tools.web.celery.debug_task')
@no_simultaneous_execution(retry=60)
def debug_task(self):
    logger.info('sleeping 10 seconds')
    from time import sleep
    sleep(10)
    logger.info("debug task executed")


@app.task(bind=True, name='mm_tools.web.celery.import_logs')
@no_simultaneous_execution(retry=60*5)
def import_logs(self):
    from .warcraft_logs.tasks import process_new_reports
    process_new_reports()
