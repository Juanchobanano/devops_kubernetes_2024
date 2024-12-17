from fastapi import FastAPI, Depends
from sqlmodel import Session, select
import uvicorn
import utils
import constants as ct
from typing import Annotated
from models import Todo, TodoModel

SessionDep = Annotated[Session, Depends(lambda: utils.get_session(ct.engine))]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    utils.create_db_and_tables(ct.engine)


@app.get("/todos")
async def get_todos(session: SessionDep):
    session_ = next(session)
    statement = select(Todo)
    results = session_.exec(statement)
    todos = [x.description for x in results.all()]
    return {"todos": todos}


@app.post("/todos")
async def create_todo(session: SessionDep, todo: TodoModel):
    session_ = next(session)
    todo_obj = Todo(description=todo.description)
    session_.add(todo_obj)
    session_.commit()
    session_.close()
    return {"message": "Todo created successfully", "todo": todo}


if __name__ == "__main__":
    print(f"Server started on port {ct.PORT}")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=ct.PORT,
        reload=True)
