import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

from app.database import Base, engine

client = TestClient(app)

DATABASE_TEST_URL = 'postgresql://postgres:password@localhost:5434/postgres'
engine = sqlalchemy.create_engine(DATABASE_TEST_URL)
test_session = Session(engine)


# docker run --name test_postgres -e POSTGRES_PASSWORD=password -p 5434:5432 postgres

def get_test_db():
    try:
        yield test_session
        test_session.commit()
    except:
        raise NotImplementedError()
    finally:
        test_session.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
