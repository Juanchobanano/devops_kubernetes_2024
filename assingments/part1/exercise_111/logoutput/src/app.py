# reader.py
import hashlib
import os
from fastapi import FastAPI
import uvicorn
import datetime
from fastapi.responses import PlainTextResponse


directory = os.path.join('/', 'usr', 'src', 'app', 'files')
file_path = f"{directory}/log.txt"
PORT = int(os.environ.get("PORT", 8000))

app = FastAPI()


def compute_hash(line):
    return hashlib.sha256(line.encode()).hexdigest()


@app.get("/", response_class=PlainTextResponse)
def home():
    try:
        timestamp = datetime.datetime.now().isoformat()
        with open(file_path, "r") as file:
            lines = file.readlines()
            last_line = lines[-1]
            return f"{timestamp} -> {compute_hash(last_line)}\n{last_line}"
    except FileNotFoundError:
        return "Waiting for the file..."


if __name__ == '__main__':
    # Run the FastAPI app on port 8000
    uvicorn.run(app, host='0.0.0.0', port=PORT)
