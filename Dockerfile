FROM python:3.10.11-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update &&  \
    apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers \
    && apk add libffi-dev

COPY requirements.txt /app/

RUN pip install -r requirements.txt && \
    pip install gunicorn==20.1.0

RUN apk del .tmp-build-deps && rm -rf /var/cache/apk/*

ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
ENV TZ=America/Sao_Paulo