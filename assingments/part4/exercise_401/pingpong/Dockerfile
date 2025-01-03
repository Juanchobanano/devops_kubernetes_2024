# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Set environment variable to disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install curl
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y postgresql-client

# Install any necessary dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --upgrade wheel && \
    pip install --upgrade setuptools && \
    pip install fastapi uvicorn sqlmodel

RUN pip install psycopg2-binary

# Run the FastAPI server
CMD ["python", "app.py"]