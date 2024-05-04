import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


url = 'postgresql://postgres:123@localhost:5432/endterm_db'

engine = sqlalchemy.create_engine(url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
