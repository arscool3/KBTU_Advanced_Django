import pytest
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker

from fastapi.testclient import TestClient

from main import app

from database import Base, engine, get_db
from schemas import *
from config import settings

client = TestClient(app)

url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/test_practice_7'
engine = sqlalchemy.create_engine(url)
test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_session():
    db = test_session()
    try:
        yield db
        db.commit()
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_session


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_genre(test_db):
    response = client.get("/genre")
    assert response.json() == []


# def test_add_genre(test_db):
#     response = client.post("/genre", json={'name': 'drama'})
#     assert response.status_code == 200
#     response = client.get("/genre")
#     assert response.json() == [{'id': 1, 'name': 'drama'}]
#
#
# # def test_get_director
#
# def test_get_director(test_db):
#     response = client.get("/director")
#     assert response.json() == []
#
#
# def test_add_director(test_db):
#     response = client.post('/director', json={'name': 'TestDirector!'})
#     assert response.status_code == 200
#     response = client.get('/director')
#     assert response.json() == [{'id': 1, 'name': 'TestDirector!'}]
#
#
# # test films
#
# def test_get_film(test_db):
#     response = client.get("/film")
#     assert response.json() == []
#
#
# def test_add_film(test_db):
#     client.post('/director', json={'name': 'testDirector'})
#     client.post('/genre', json={'name': 'testGenre'})
#     response = client.post("/film", json={
#         'director_id': 1,
#         'genre_id': 1,
#         'name': 'FILMFILM'
#     })
#
#     # created_film = schemas.CreateMovie(**response.json())
#
#     assert response.status_code == 200
#     # assert created_film.name == 'FILMFILM'
#     # assert created_film.genre_id == 1
#     # assert created_film.director_id == 1
#     response = client.get('/films')
#     # assert response.json() == [{
#     #     'director_id': 1,
#     #     'genre_id': 1,
#     #     'name': 'FILMFILM'
#     # }]
