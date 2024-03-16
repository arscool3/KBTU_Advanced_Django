from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session

from database import session
from schemas import (
    UserCreate,
    AccountCreate,
    PaymentCreate,
    LoanCreate,
    TransactionCreate,
    SecurityCreate
)
from repository import (
    UserRepository,
    AccountRepository,
    PaymentRepository,
    LoanRepository,
    TransactionRepository,
    SecurityRepository
)

app = FastAPI()


# class DBSession:
#     async def __init__(self):
#         self._db = None
#
#     async def get_session(self):
#         if self._db is None:
#             self._db = session
#         return self._db
#
#
# db_session = DBSession()


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


user_repo = UserRepository(session)
account_repo = AccountRepository(session)
payment_repo = PaymentRepository(session)
loan_repo = LoanRepository(session)
transaction_repo = TransactionRepository(session)
security_repo = SecurityRepository(session)


@app.post("/users")
async def create_user(data: UserCreate, db_session: Session = Depends(get_db)):
    return user_repo.create(db_session, data)


@app.get("/user/{user_id}")
async def get_user(user_id: int, db_session: Session = Depends(get_db)):
    return user_repo.get(db_session, user_id)


@app.get("/users/all")
async def get_users(db_session: Session = Depends(get_db)):
    return user_repo.get_all(db_session)


@app.post("/accounts")
async def create_account(data: AccountCreate, db_session: Session = Depends(get_db)):
    return account_repo.create(db_session, data)


@app.get("/account/{account_id}")
async def get_account(account_id: int, db_session: Session = Depends(get_db)):
    return account_repo.get(db_session, account_id)


@app.get("/accounts/all")
async def get_accounts(db_session: Session = Depends(get_db)):
    return account_repo.get_all(db_session)


@app.post("/payments")
async def create_payment(data: PaymentCreate, db_session: Session = Depends(get_db)):
    return payment_repo.create(db_session, data)


@app.get("/payment/{payment_id}")
async def get_payment(payment_id: int, db_session: Session = Depends(get_db)):
    return payment_repo.get(db_session, payment_id)


@app.get("/payments/all")
async def get_payments(db_session: Session = Depends(get_db)):
    return payment_repo.get_all(db_session)


@app.post("/loans")
async def create_loan(data: LoanCreate, db_session: Session = Depends(get_db)):
    return loan_repo.create(db_session, data)


@app.get("/loan/{loan_id}")
async def get_loan(loan_id: int, db_session: Session = Depends(get_db)):
    return loan_repo.get(db_session, loan_id)


@app.get("/loans/all")
async def get_loans(db_session: Session = Depends(get_db)):
    return loan_repo.get_all(db_session)


@app.post("/transactions")
async def create_transaction(data: TransactionCreate, db_session: Session = Depends(get_db)):
    return transaction_repo.create(db_session, data)


@app.get("/transaction/{transaction_id}")
async def get_transaction(transaction_id: int, db_session: Session = Depends(get_db)):
    return transaction_repo.get(db_session, transaction_id)


@app.get("/transactions/all")
async def get_transactions(db_session: Session = Depends(get_db)):
    return transaction_repo.get_all(db_session)


@app.post("/security")
async def create_security(data: SecurityCreate, db_session: Session = Depends(get_db)):
    return security_repo.create(db_session, data)


@app.get("/security/{security_id}")
async def get_security(security_id: int, db_session: Session = Depends(get_db)):
    return security_repo.get(db_session, security_id)


@app.get("/securities/all")
async def get_securities(db_session: Session = Depends(get_db)):
    return security_repo.get_all(db_session)
