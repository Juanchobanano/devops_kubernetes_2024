from sqlmodel import Field, SQLModel


# Define the Counter model
class Counter(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    count: int = Field(default=None, index=True)
