# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Set environment variable to disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Install curl
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y postgresql-client

# Install any necessary dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install fastapi uvicorn requests jinja2 pydantic

# Run the FastAPI server
CMD ["python", "app.py"]