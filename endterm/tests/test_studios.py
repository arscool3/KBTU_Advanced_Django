import pytest

from app import schemas


def test_get_all_studios(client, test_studio):
    res = client.get('/studio/')

    def validate(studio):
        return schemas.Studio(**studio)

    studio_map = map(validate, res.json())

    studio_list = list(studio_map)

    # assert len(res.json()) == len(test_genre)
    assert res.status_code == 200


def test_get_studios_by_id(client, test_studio):
    res = client.get(f'/studio/{test_studio["id"]}')
    studio = schemas.Studio(**res.json())
    assert studio.name == test_studio['name']


# def test_get_genre_not_exist(client, test_genre):
#     res = client.get('/genre/9999999')
#     assert res.status_code == 500

def test_create_studio(client):

    res = client.post('/studio/', json={
        'name': "20FOX TEST"
    })

    created_studio = schemas.Studio(**res.json())

    assert res.status_code == 200

def test_delete_studio(client, test_studio):
    res = client.delete(f'/genre/{test_studio["id"]}')
    assert res.status_code == 200