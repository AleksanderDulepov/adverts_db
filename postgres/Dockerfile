FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN apt update -y && apt install -y libpq-dev gcc && pip install -r requirements.txt
COPY . .