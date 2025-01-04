from sqlmodel import Session, SQLModel, select
from models import Counter


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def get_session(engine):
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def create_counter(engine):
    with Session(engine) as session:
        statement = select(Counter).where(Counter.id == 1)
        results = session.exec(statement)
        counter = results.one_or_none()
        if not counter:
            counter = Counter(id=1, count=0)
            session.add(counter)
            session.commit()
