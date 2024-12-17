# reader.py
import hashlib
import os
from fastapi import FastAPI
import uvicorn
import datetime
from fastapi.responses import PlainTextResponse
import requests

PORT = int(os.environ.get("PORT", 8005))
PINGPONG_HOST = os.environ.get("PINGPONG_HOST", "localhost")
PINGPONG_PORT = int(os.environ.get("PINGPONG_PORT", 8000))
PINGPONG_ENDPOINT = f"http://{PINGPONG_HOST}:{PINGPONG_PORT}/pingpong"

app = FastAPI()


def compute_hash(line):
    return hashlib.sha256(line.encode()).hexdigest()


@app.get("/", response_class=PlainTextResponse)
def home():
    timestamp = datetime.datetime.now().isoformat()
    pingpong_data = requests.get(PINGPONG_ENDPOINT).text
    return f"{timestamp} -> {compute_hash(pingpong_data)}\n{pingpong_data}"


if __name__ == '__main__':
    # Run the FastAPI app on port 8000
    uvicorn.run(app, host='0.0.0.0', port=PORT)
