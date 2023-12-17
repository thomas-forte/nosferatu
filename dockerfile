FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \
    && apk upgrade\
    && apk add --update --no-cache gcc musl-dev

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
