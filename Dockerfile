FROM docker.iranserver.com/python:3.13.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip gunicorn && \
    pip install -r requirements.txt
COPY . /app
RUN chmod +x /app/scripts/*.sh
RUN apt-get update
RUN apt-get install curl -y
EXPOSE 8000

CMD ["bash", "/app/scripts/start_web.sh"]
