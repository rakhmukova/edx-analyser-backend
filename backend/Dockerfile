FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /config
RUN mkdir /src

COPY requirements.txt /config/requirements.txt

RUN pip install -r /config/requirements.txt

WORKDIR /src
