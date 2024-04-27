import pytest
from starlette import status

from app import schemas


def test_get_all_movies(client, test_movies):
    res = client.get('/movie/')

    def validate(movie):
        return schemas.Movie(**movie)

    movies_map = map(validate, res.json())
    movie_list = list(movies_map)

    assert len(res.json()) == len(test_movies)
    assert res.status_code == 200


def test_get_movie_by_id(client, test_movies):
    res = client.get(f'/movie/{test_movies[0].id}')

    movie = schemas.Movie(**res.json())
    assert movie.name == test_movies[0].name


# def test_get_movie_not_exists(client, test_movies):
#     res = client.get(f'/movie/9999999999')
#     assert res.status_code == 404


def test_create_movie(client, test_movies):
    res = client.post('/movie/', json={
        "name": "Test Bakytzhan NEW",
        "director_id": 1,
        "genre_id": 1,
        "studio_id": 1,
        "rating": 0
    })

    created_movie = schemas.Movie(**res.json())
    assert res.status_code == 200


def test_success_delete_movie(client, test_movies):
    res = client.delete(f'/movie/{test_movies[0].id}')
    assert res.status_code == 200


def test_delete_movie_non_exist(client, test_movies):
    res = client.delete(f'/movie/9999999')
    assert res.status_code == 200



