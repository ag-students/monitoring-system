FROM python:3.8-slim

ENV PROJECT_ROOT=/monitoring-server

WORKDIR $PROJECT_ROOT

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY .flaskenv monitoring-server.py $PROJECT_ROOT/

ENV FLASK_APP = monitoring-server.py

EXPOSE 5000
