from sqlmodel import Field, SQLModel
from pydantic import BaseModel


# Define the Counter model
class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(default=None, index=True)
    done: bool = Field(default=False)


# Data model for a Todo item
class TodoModel(BaseModel):
    description: str
