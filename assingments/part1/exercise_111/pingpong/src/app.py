from fastapi import FastAPI
import uvicorn
import os
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Directory and file path for shared volume
PORT = int(os.environ.get("PORT", 8000))
directory = os.path.join('/', 'usr', 'src', 'app', 'files')
log_file = os.path.join(directory, "log.txt")


@app.get("/pingpong", response_class=PlainTextResponse)
def pingpong():
    """Increment counter and save to log file."""
    counter = 0

    # Read the existing counter
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                counter = int(last_line.split(":")[1].strip())

    # Increment the counter and append to the file
    counter += 1
    output = f"Ping / Pongs: {counter}\n"

    try:
        with open(log_file, "a") as file:
            file.write(output)
        return output
    except Exception:
        return "Error writing to file"


if __name__ == '__main__':
    # Run the FastAPI app on port 8000
    uvicorn.run(app, host='0.0.0.0', port=PORT)
