pip install gevent

celery -A core beat -l info --pool=gevent
