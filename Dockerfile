FROM python:3.11-alpine

RUN apk add bash

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ARG EFFORT_DEBUG='False'
ARG EFFORT_STATIC_ROOT='/static-root'
ARG EFFORT_ALLOWED_HOSTS='0.0.0.0'
ARG EFFORT_DATABASE_ENGINE='sqlite3'
ARG EFFORT_SQLITE3_PATH='/db.sqlite3'
ARG EFFORT_POSTGRES_SERVICE='/pgservice'
ARG EFFORT_POSTGRES_PASSFILE='/.pgpass'

ENV EFFORT_DEBUG=${EFFORT_DEBUG}
ENV EFFORT_SECRET_KEY=${EFFORT_SECRET_KEY}
ENV EFFORT_STATIC_ROOT=${EFFORT_STATIC_ROOT}
ENV EFFORT_ALLOWED_HOSTS=${EFFORT_ALLOWED_HOSTS}
ENV EFFORT_DATABASE_ENGINE=${EFFORT_DATABASE_ENGINE}
ENV EFFORT_SQLITE3_PATH=${EFFORT_SQLITE3_PATH}
ENV EFFORT_POSTGRES_SERVICE=${EFFORT_POSTGRES_SERVICE}
ENV EFFORT_POSTGRES_PASSFILE=${EFFORT_POSTGRES_PASSFILE}

EXPOSE 8000/

ENTRYPOINT python manage.py migrate \
    && python manage.py collectstatic --no-input \
    && honcho start