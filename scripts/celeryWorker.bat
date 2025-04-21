pip install gevent

celery -A core worker -l info -P gevent
