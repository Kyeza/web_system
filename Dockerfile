FROM python:3.8-slim-buster
MAINTAINER Kyeza M. Arnold

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y --fix-missing \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info

RUN groupadd -r celery && useradd --no-log-init -r -g celery celery

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/