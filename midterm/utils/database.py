from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

url = 'postgresql://postgres:123456@localhost/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()


def get_db():
    try:
        yield session
        session.commit()
    except Exception as e:
        raise
    finally:
        session.close()
