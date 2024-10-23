FROM python:3.12

WORKDIR /core

COPY requirements.txt /core/

RUN pip install -r requirements.txt

COPY . /core/