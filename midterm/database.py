from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(url)


def get_db():
    try:
        session = Session(engine)
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()
