import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = 'postgresql://postgres:password@localhost:5433/postgres'
engine = sqlalchemy.create_engine(url)
session = Session(engine)
Base = declarative_base()


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()
