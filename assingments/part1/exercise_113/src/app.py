from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os
import time
import requests
import uvicorn


app = FastAPI()

# Paths and constants
CACHE_DIR = os.path.join('/', 'usr', 'src', 'app', 'files')
IMAGE_PATH = os.path.join(CACHE_DIR, "cached_image.jpg")
CACHE_EXPIRY = 3600  # 60 minutes in seconds
PORT = int(os.getenv("PORT", 8000))

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
async def root(request: Request):
    get_cached_image()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "image_url": "/image"},
    )


@app.get("/image")
async def get_image():
    """Serve the cached image."""
    get_cached_image()
    return FileResponse(IMAGE_PATH, media_type="image/jpeg")


if __name__ == "__main__":
    print(f"Server started on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
