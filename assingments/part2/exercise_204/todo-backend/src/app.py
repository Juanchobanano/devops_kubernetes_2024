from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()
PORT = int(os.environ.get("PORT", 9030))

# In-memory storage for todos
todos = [
    "Task 1",
    "Task 2",
    "Task 3"
]


# Data model for a Todo item
class TodoItem(BaseModel):
    description: str


@app.get("/todos")
async def get_todos():
    """
    Retrieve all todos.
    """
    global todos
    return {"todos": todos}


@app.post("/todos")
async def create_todo(todo: TodoItem):
    """
    Create a new todo item.
    """
    # Add the new todo
    todos.append(todo.description)
    return {"message": "Todo created successfully", "todo": todo}


if __name__ == "__main__":
    print(f"Server started on port {PORT}")
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
