FROM python:3.11-slim

WORKDIR /app

COPY ./analytics-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./analytics-api .