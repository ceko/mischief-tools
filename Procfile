web:        gunicorn mm_tools.web.wsgi:application
worker:     celery -A mm_tools.web worker -B -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
release:    bash ./release