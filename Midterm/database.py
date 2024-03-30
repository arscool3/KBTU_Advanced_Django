from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker


url = f"postgresql://postgres:December1225@localhost/midterm_2"
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