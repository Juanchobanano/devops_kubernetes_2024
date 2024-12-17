from fastapi import FastAPI
import uvicorn
import os
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Directory and file path for shared volume
PORT = int(os.environ.get("PORT", 8000))
counter = 0


@app.get("/pingpong", response_class=PlainTextResponse)
def pingpong():
    global counter

    # Increment the counter and append to the file
    counter += 1
    output = f"Ping / Pongs: {counter}\n"
    return output


if __name__ == '__main__':
    # Run the FastAPI app on port 8000
    uvicorn.run(app, host='0.0.0.0', port=PORT)
