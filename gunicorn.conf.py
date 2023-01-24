import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('GUNICORN_PORT')}"
workers = multiprocessing.cpu_count() * 2 + 1
