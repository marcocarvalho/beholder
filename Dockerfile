FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

RUN apk add --no-cache build-base python-dev curl libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev

RUN pip install scrapy

CMD sh
