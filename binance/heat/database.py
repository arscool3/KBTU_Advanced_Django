
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

url = "postgresql://postgres:December1225@localhost/binance"
engine = create_engine(url)
session = Session(engine)
Base = declarative_base()


def get_db():
    try:
        yield session
        session.commit()
    except Exception:
        raise
    finally:
        session.close()
