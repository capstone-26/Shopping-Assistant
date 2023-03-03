FROM python:3.11.0a5-alpine3.14

# Ensures that we get the unbuffered python output
ENV PYTHONUNBUFFERED=1

WORKDIR /django

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt