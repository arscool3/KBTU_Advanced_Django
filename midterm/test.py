import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .main import app, get_db
import database as db
from models import Base
import models
import schemas

client = TestClient()

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = sqlalchemy.create_engine(url)
Base.metadata.create_all(bind=engine)
test_session = Session(engine)


# def get_test_db():
#     try:
#         yield test_session
#         test_session.commit()
#     except:
#         raise
#     finally:
#         test_session.close()
#
#
# app.dependency_overrides[get_db] = get_test_db
#
#
# @pytest.fixture
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)
#
#
def test(test_db):
    response = client.get('/jobs')
    assert response.json() == []