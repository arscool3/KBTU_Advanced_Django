from datetime import date

from tests.test_accounts import test_add_account
from tests.test_categories import test_add_category
from tests.test_database import client
from tests.test_database import test_db


def test_get_expenses(test_db):
    response = client.get("/expense/get_expenses")
    assert response.json() == []


def test_add_expense(test_db):
    test_add_account(test_db=test_db)
    test_add_category(test_db=test_db)

    response = client.post("/expense/create_expense", json={
        'user_id': 1,
        'account_id': 1,
        'category_id': 1,
        'amount': 500.0,
        'description': 'something and so',
        'expense_date': f'{date.today()}'
    })
    assert response.status_code == 200