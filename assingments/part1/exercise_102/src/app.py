from fastapi import FastAPI
import uvicorn
import os

# Create an instance of FastAPI
app = FastAPI()

# Define the port from an environment variable or use a default
PORT = int(os.getenv("PORT", 8000))


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}


if __name__ == "__main__":
    print(f"Server started on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
