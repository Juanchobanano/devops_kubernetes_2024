from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn
import os

app = FastAPI()
PORT = int(os.getenv("PORT", 8000))

# In-memory counter
counter = 0


@app.get('/pingpong', response_class=PlainTextResponse)
def pingpong():
    global counter
    response = f"pong {counter}"
    counter += 1
    return response


if __name__ == '__main__':
    # Run the FastAPI app on port 5000
    uvicorn.run(app, host='0.0.0.0', port=PORT)
