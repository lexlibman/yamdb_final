FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/usr/src/web

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt ./

RUN python3 -m pip install --upgrade pip \
    && pip3 install -r requirements.txt --no-cache-dir

WORKDIR $APP_HOME
COPY . $APP_HOME

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000