from .settings import *

REMOVE_MIDDLEWARE = ['silk.middleware.SilkyMiddleware',
                     "debug_toolbar.middleware.DebugToolbarMiddleware"]
for i in REMOVE_MIDDLEWARE:
    try:
        MIDDLEWARE.remove(i)
    except IndexError:
        ...


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
