from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url = 'postgresql://postgres:postgres@localhost:5432/lesson6'
engine = create_engine(url)


def get_db():
    dbb = Session(engine)
    try:
        yield dbb
    finally:
        dbb.close()

