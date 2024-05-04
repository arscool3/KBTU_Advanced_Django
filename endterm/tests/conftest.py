import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app import models

from app.config import settings
from app.database import get_db, Base
from app.main import app
from app.models import Director, Genre, Studio

SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}@'
                           f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test')
engine = create_engine(SQLALCHEMY_DATABASE_URL)

test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = test_session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_studio(session):
    studio_data = {
        "id": '1',
        "name": "Ghibli",
    }

    session.add(Studio(**studio_data))
    session.commit()

    return studio_data

@pytest.fixture
def test_genre(session):
    genre_data = {
        "id": '1',
        "name": "Drama",
    }

    session.add(Genre(**genre_data))
    session.commit()

    return genre_data

@pytest.fixture
def test_director(session):
    directors_data = {
        "id": '1',
        "name": "Bakytzhan",
    }

    session.add(Director(**directors_data))
    session.commit()

    return directors_data

@pytest.fixture
def test_movies(session, test_director, test_genre, test_studio):
    movies_data = [
        {
            "name": "first",
            "director_id": 1,
            "genre_id": 1,
            "studio_id": 1,
            "rating": 0
        }, {
            "name": "second",
            "director_id": 1,
            "genre_id": 1,
            "studio_id": 1,
            "rating": 0
        }

    ]

    def create_movie_model(movie):
        return models.Movie(**movie)

    movie_map = map(create_movie_model, movies_data)
    movies = list(movie_map)

    session.add_all(movies)
    session.commit()

    movies = session.query(models.Movie).all()
    return movies
