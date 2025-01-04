from sqlmodel import Session, SQLModel
import nats
import constants as ct
import json
from models import Todo


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def get_session(engine):
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


async def publish_to_nats(action, todo: Todo):
    client = await nats.connect(ct.NATS_ENDPOINT)
    message = {
        "action": action,
        "todoId": todo.id,
        "description": todo.description,
        "done": todo.done
    }
    await client.publish(
        "todos.status",
        json.dumps(message).encode())
    await client.close()
