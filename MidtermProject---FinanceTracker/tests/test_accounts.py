
from tests.test_database import client
from tests.test_users import test_add_user
from tests.test_database import test_db


def test_get_accounts(test_db):
    response = client.get("/account/get_accounts")
    assert response.json() == []


def test_add_account(test_db):
    test_add_user(test_db)

    response = client.post("/account/create_account", json={
        'account_name': 'ALLETttttt',
        'account_type': 'deposit',
        'user_id': 1
    })
    assert response.status_code == 200

    response = client.get("/account/get_accounts")
    assert response.json() == [
        {
            'account_name': 'ALLETttttt',
            'account_type': 'deposit',
            'id': 1,
            'transactions': []
        }
    ]
