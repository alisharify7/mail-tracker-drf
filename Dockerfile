FROM docker.iranserver.com/python:3.13.3-alpine3.21

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip gunicorn && \
    pip install -r requirements.txt

COPY . /app

RUN python manage.py makemigrations
RUN python manage.py migrate

#TODO: instead of running migrations and running app in docker file create an entrypoint script for this
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]