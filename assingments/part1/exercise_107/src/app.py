import uvicorn
from fastapi import FastAPI
from datetime import datetime
import random
import string
import os

PORT = int(os.getenv("PORT", 8000))


app = FastAPI()

# Store the timestamp and string in memory
status = {
    "timestamp": None,
    "string": None,
}


def generate_random_string(length=8):
    """Generate a random string of given length."""
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits, k=length))


@app.on_event("startup")
async def startup_event():
    """Initialize the status on application startup."""
    update_status()


def update_status():
    """Update the timestamp and string."""
    status["timestamp"] = datetime.utcnow().isoformat()
    status["string"] = generate_random_string()
    print(f"[LOG] {status['timestamp']} - {status['string']}")


@app.get("/status")
async def get_status():
    """Return the current status."""
    return status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
