# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV CELERY_BROKER_URL="amqp://rabbitmq:rabbitmq@rabbitmq:5672"
ENV DATABASE_URL="postgresql://postgres:postgres@discount-db/app"


COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /worker
WORKDIR /worker

ENTRYPOINT celery -A tasks worker --loglevel=info
