from .settings import *

REMOVE_MIDDLEWARE = ['silk.middleware.SilkyMiddleware',
                     "debug_toolbar.middleware.DebugToolbarMiddleware"]
for i in REMOVE_MIDDLEWARE:
    try:
        MIDDLEWARE.remove(i)
    except IndexError:
        ...


CELERY_TASK_ALWAYS_EAGER = True