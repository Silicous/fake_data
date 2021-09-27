web: gunicorn --chdir fake_data.wsgi --log-file -
worker: celery --app core.celery worker
