from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import os

# Create an instance of FastAPI
app = FastAPI()

# Define the port from an environment variable or use a default
PORT = int(os.getenv("PORT", 8000))


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI HTML Page</title>
    </head>
    <body>
        <h1>Welcome to the FastAPI Server!</h1>
        <p>This is an example of serving HTML content with FastAPI.</p>
    </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    print(f"Server started on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
