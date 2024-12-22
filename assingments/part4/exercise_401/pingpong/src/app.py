from fastapi import FastAPI, Depends
from sqlmodel import Session, select
import uvicorn
from fastapi.responses import PlainTextResponse
import utils
import constants as ct
from typing import Annotated
from models import Counter

SessionDep = Annotated[Session, Depends(lambda: utils.get_session(ct.engine))]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    utils.create_db_and_tables(ct.engine)
    utils.create_counter(ct.engine)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Hello World!"


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "App working!"


@app.get("/pingpong", response_class=PlainTextResponse)
async def pingpong(session: SessionDep):
    # Fetch the current counter from the database
    session_ = next(session)
    statement = select(Counter).where(Counter.id == 1)
    results = session_.exec(statement)
    counter = results.one_or_none()

    counter.count += 1
    session_.add(counter)
    session_.commit()
    session_.refresh(counter)

    # Return the incremented counter
    return f"Ping / Pongs: {counter.count}\n"


if __name__ == '__main__':
    # Run the FastAPI app on port 8000
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=ct.PORT,
        reload=True)
