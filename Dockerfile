# syntax=docker/dockerfile:1
FROM python:3.9-alpine3.13
LABEL maintainer="https://github.com/King-Greatman-Spirit"

ENV PYTHONUNBUFFERED=1

COPY . /app
WORKDIR /app

# create the app user
# RUN adduser --disabled-password --no-create-home ws

# USER ws

RUN python3 -m venv /opt/venv

RUN apk add -u zlib-dev jpeg-dev gcc musl-dev && \
    /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
