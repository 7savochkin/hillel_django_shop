from time import sleep

from django.core.cache import cache

from shop.celery import app


@app.task(bind=True, default_retry_delay=30)
def task_task(self, x, y):
    print('TEST BEFORE')
    sleep(5)
    try:
        x['key']
    except (KeyError, TypeError) as exc:
        raise self.retry(exc=exc, countdown=5)
    print('TEST AFTER')
    return x+y