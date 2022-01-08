# syntax=docker/dockerfile:1

FROM python:3.10.0rc2-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN apt-get update
RUN apt-get upgrade


RUN apt-get install -y zlib1g-dev
RUN pip3 install -r requirements.txt

COPY ./docker_domain .