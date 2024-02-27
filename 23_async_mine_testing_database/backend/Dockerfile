FROM python:3.12-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y libpq-dev

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .
