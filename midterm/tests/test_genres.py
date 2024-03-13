import pytest

from app import schemas


def test_get_all_genres(client, test_genre):
    res = client.get('/genre/')

    def validate(genre):
        return schemas.Genre(**genre)

    genre_map = map(validate, res.json())

    genre_list = list(genre_map)

    # assert len(res.json()) == len(test_genre)
    assert res.status_code == 200


def test_get_genre_by_id(client, test_genre):
    res = client.get(f'/genre/{test_genre["id"]}')
    genre = schemas.Genre(**res.json())
    assert genre.name == test_genre['name']


# def test_get_genre_not_exist(client, test_genre):
#     res = client.get('/genre/9999999')
#     assert res.status_code == 500

def test_create_genre(client):

    res = client.post('/genre/', json={
        'name': "Comedy TEST"
    })

    created_genre = schemas.Genre(**res.json())

    assert res.status_code == 200

def test_delete_genre(client, test_genre):
    res = client.delete(f'/genre/{test_genre["id"]}')
    assert res.status_code == 200