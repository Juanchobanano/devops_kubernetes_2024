# reader.py
import hashlib
import os
from fastapi import FastAPI
import uvicorn
import datetime
from fastapi.responses import PlainTextResponse
import requests

MESSAGE = os.environ.get("MESSAGE", "Message not found!")
PORT = int(os.environ.get("PORT", 8005))
PINGPONG_HOST = os.environ.get("PINGPONG_HOST", "localhost")
PINGPONG_PORT = int(os.environ.get("PINGPONG_PORT", 8000))
PINGPONG_ENDPOINT = f"http://{PINGPONG_HOST}:{PINGPONG_PORT}/pingpong"

app = FastAPI()


def compute_hash(line):
    return hashlib.sha256(line.encode()).hexdigest()


def read_file_text():
    with open('/config/serverconfig.txt', 'r') as f:
        for line in f:
            if line.startswith('text='):
                text_value = line.split('=', 1)[1].strip()
                return text_value


@app.get("/", response_class=PlainTextResponse)
def home():
    text_value = read_file_text()
    timestamp = datetime.datetime.now().isoformat()
    pingpong_data = requests.get(PINGPONG_ENDPOINT).text
    response = (
        f"file content: {text_value}\n"
        f"env variable: MESSAGE={MESSAGE}\n"
        f"{timestamp} -> "
        f"{compute_hash(pingpong_data)}\n{pingpong_data}"
    )
    return response


if __name__ == '__main__':
    # Run the FastAPI app on port 8000
    uvicorn.run(app, host='0.0.0.0', port=PORT)
