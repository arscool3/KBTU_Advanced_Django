from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

url = 'postgresql://postgres:yerkhan2003@localhost/postgres'
engine = create_engine(url)
session = Session(engine)
Base = declarative_base()


@contextmanager
def get_db():
    try:
        yield session
        session.commit()
    except Exception as e:
        raise
    finally:
        session.close()