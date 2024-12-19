from sqlmodel import Session, SQLModel


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def get_session(engine):
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
