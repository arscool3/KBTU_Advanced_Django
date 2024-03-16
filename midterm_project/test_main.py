from datetime import datetime

import pytest

from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

client = TestClient(app)

url = 'postgresql://postgres:admin@localhost/test_postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_users(test_db):
    response = client.get("/users/all")
    assert response.json() == []


def test_create_user(test_db):
    response = client.post("/users", json={'id': 2,
                                           'name': 'Test2 User',
                                           'email': 'test2@example.com',
                                           'phone_number': '1234567899'})
    assert response.status_code == 200
    response = client.get("/user/2")
    assert response.json() == [{'id': 2,
                                'name': 'Test2 User',
                                'email': 'test2@example.com',
                                'phone_number': '1234567899'}]


def test_get_accounts(test_db):
    response = client.get("/accounts/all")
    assert response.json() == []


def test_create_account(test_db):
    response = client.post("/accounts", json={'id': 2,
                                              'account_number': 2,
                                              'account_type': 'deposit',
                                              'balance': 10000,
                                              'user_id': 2})
    assert response.status_code == 200
    response = client.get("/account/2")
    assert response.json() == [{'id': 2,
                                'account_number': 2,
                                'account_type': 'deposit',
                                'balance': 10000,
                                'user_id': 2}]


def test_get_transactions(test_db):
    response = client.get("/transactions/all")
    assert response.json() == []


def test_create_transaction(test_db):
    timestamp = datetime.now().isoformat()
    response = client.post("/transactions", json={'id': 2,
                                                  'transaction_type': 'debit',
                                                  'amount': 5000,
                                                  'timestamp': timestamp,
                                                  'source': '1234567890',
                                                  'destination': '0987654321',
                                                  'account_id': 2})
    assert response.status_code == 200
    response = client.get("/transaction/2")
    assert response.json() == [{'id': 2,
                                'transaction_type': 'debit',
                                'amount': 5000,
                                'timestamp': timestamp,
                                'source': '1234567890',
                                'destination': '0987654321',
                                'account_id': 2}]


def test_get_loans(test_db):
    response = client.get("/loans/all")
    assert response.json() == []


def test_create_loan(test_db):
    start_date = datetime.now().isoformat()
    response = client.post("/loans", json={'id': 2,
                                           'loan_amount': 10000,
                                           'interest_rate': 0.05,
                                           'start_date': start_date,
                                           'term': 12,
                                           'purpose': 'home improvement',
                                           'late_fee': 500,
                                           'user_id': 2})
    assert response.status_code == 200
    response = client.get("/loan/2")
    assert response.json() == [{'id': 2,
                                'loan_amount': 10000,
                                'interest_rate': 0.05,
                                'start_date': start_date,
                                'term': 12,
                                'purpose': 'home improvement',
                                'late_fee': 500,
                                'user_id': 2}]


def test_get_securities(test_db):
    response = client.get("/securities/all")
    assert response.json() == []


def test_create_security(test_db):
    response = client.post("/security", json={'id': 2,
                                              'username': 'test_user2',
                                              'password': 'test_password',
                                              'user_id': 2})
    assert response.status_code == 200
    response = client.get("/security/2")
    assert response.json() == [{'id': 2,
                                'username': 'test_user2',
                                'password': 'test_password',
                                'user_id': 2}]
