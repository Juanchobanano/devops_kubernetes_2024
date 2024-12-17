from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import os
import time
import requests
import uvicorn

app = FastAPI()

PORT = int(os.getenv("PORT", 8000))
CACHE_DIR = os.path.join('/', 'usr', 'src', 'app', 'files')
IMAGE_PATH = os.path.join(CACHE_DIR, "cached_image.jpg")
CACHE_EXPIRY = 3600  # 60 minutes in seconds


def fetch_image():
    """Fetch a new image from Lorem Picsum and save it locally."""
    response = requests.get("https://picsum.photos/1200", stream=True)
    if response.status_code == 200:
        with open(IMAGE_PATH, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print("Fetched and cached a new image.")
    else:
        print("Failed to fetch the image. Status code:", response.status_code)


def get_cached_image():
    """Ensure the cached image is valid (not expired).
    Fetch a new one if needed."""
    if not os.path.exists(IMAGE_PATH):
        fetch_image()
    else:
        last_modified = os.path.getmtime(IMAGE_PATH)
        if time.time() - last_modified > CACHE_EXPIRY:
            fetch_image()


@app.get("/", response_class=HTMLResponse)
async def root():
    get_cached_image()
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Image Cache</title>
    </head>
    <body>
        <h1>Welcome to the FastAPI Server!</h1>
        <p>This is an example of serving a cached image that updates every hour.</p>
        <img src="/image" alt="Random Image" style="max-width: 30%; height: auto;">
    </body>
    </html>
    """
    return html_content


@app.get("/image")
async def get_image():
    get_cached_image()
    return FileResponse(IMAGE_PATH, media_type="image/jpeg")


if __name__ == "__main__":
    print(f"Server started on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
