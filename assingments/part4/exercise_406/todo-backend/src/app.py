from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from sqlmodel import Session, select
import uvicorn
import utils
import constants as ct
from typing import Annotated
from models import Todo, TodoModel
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

SessionDep = Annotated[Session, Depends(lambda: utils.get_session(ct.engine))]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    utils.create_db_and_tables(ct.engine)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Hello World!"


@app.get("/todos")
async def get_todos(session: SessionDep):
    session_ = next(session)
    statement = select(Todo)
    results = session_.exec(statement)
    todos = [{"id": x.id, "description": x.description, "done": x.done}
             for x in results.all()]
    return {"todos": todos}


@app.get("/healthz", response_class=PlainTextResponse)
async def healthz():
    return "OK"


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, session: SessionDep):
    session_ = next(session)
    todo = session_.get(Todo, todo_id)
    if todo is None:
        return {
            "message": "Todo not found",
            "status_code": 404
        }
    todo.done = not todo.done
    session_.add(todo)
    session_.commit()
    session_.close()

    await utils.publish_to_nats(
        action="update",
        todo=todo
    )

    return {
        "message": "Todo updated successfully",
        "status_code": 200
    }


@app.post("/todos")
async def create_todo(session: SessionDep, todo: TodoModel):

    todo_description = todo.description
    logger.info(f"Todo description: {todo_description}")
    if len(todo_description) > ct.MAX_CHARACTERS:
        logger.error(
            "Todo description is too long:"
            f"{len(todo_description)} characters.")
        return {
            "message": (
                "Todo description must be at most"
                f"{ct.MAX_CHARACTERS} characters long",
            ),
            "status_code": 400
        }
    session_ = next(session)
    todo_obj = Todo(
        description=todo.description,
        done=False)
    session_.add(todo_obj)
    session_.commit()
    session_.close()
    logging.info("Todo created successfully")

    await utils.publish_to_nats(
        action="create",
        todo=todo
    )

    return {
        "message": "Todo created successfully",
        "status_code": 200
    }


if __name__ == "__main__":
    print(f"Server started on port {ct.PORT}")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=ct.PORT,
        reload=True)
