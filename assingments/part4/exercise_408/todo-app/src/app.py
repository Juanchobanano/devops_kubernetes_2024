from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os
import time
import requests
import uvicorn
from pydantic import BaseModel

TODOS_HOST = os.environ.get("TODOS_HOST", "localhost")
TODOS_PORT = int(os.environ.get("TODOS_PORT", 8002))
TODOS_ENDPOINT = f"http://{TODOS_HOST}:{TODOS_PORT}/todos"


# Paths and constants
CACHE_DIR = os.path.join('/', 'usr', 'src', 'app', 'files')
IMAGE_PATH = os.path.join(CACHE_DIR, "cached_image.jpg")
CACHE_EXPIRY = 3600  # 60 minutes in seconds
PORT = int(os.getenv("PORT", 9061))

app = FastAPI()


# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Data model for a Todo item
class TodoItem(BaseModel):
    description: str


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
    todos = requests.get(TODOS_ENDPOINT).json()["todos"]
    #  get_cached_image()
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "image_url": "/image",
         "todos": todos},
    )


@app.put("/todos")
async def update_todo(request: Request):
    data = await request.json()
    todo_id = data["id"]
    _ = requests.put(f"{TODOS_ENDPOINT}/{todo_id}")


@app.post("/todos")
async def create_todo(request: Request):
    """
    Create a new todo item.
    """
    data = await request.json()
    todo_item = TodoItem(**data)
    _ = requests.post(TODOS_ENDPOINT, json=todo_item.model_dump())


@app.get("/image")
async def get_image():
    """Serve the cached image."""
    get_cached_image()
    return FileResponse(IMAGE_PATH, media_type="image/jpeg")


if __name__ == "__main__":
    print(f"Server started on port {PORT}")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=PORT,
        reload=True)
