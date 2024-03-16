from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session
import punq

from database import session
from schemas import (
    ReturnType,
    UserCreate,
    AccountCreate,
    PaymentCreate,
    LoanCreate,
    SecurityCreate,
    TransactionCreate
)
from repository import (
    BaseRepository,
    UserRepository,
    AccountRepository,
    PaymentRepository,
    LoanRepository,
    TransactionRepository,
    SecurityRepository
)

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()


# class Dependency:
#     def __init__(self, repo: BaseRepository):
#         self.repo = repo
#
#     def create(self, data) -> ReturnType:
#         return self.repo.create(data)
#
#     def get(self, item_id) -> ReturnType:
#         return self.repo.get(item_id)
#
#     def get_all(self) -> ReturnType:
#         return self.repo.get_all()
#
#
# def get_container(repository: type[BaseRepository]) -> punq.Container:
#     container = punq.Container()
#     container.register(BaseRepository, repository, instance=repository(session=session))
#     container.register(Dependency)
#     return container
#

# app.add_api_route("/users", get_container(UserRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/user/{user_id}", get_container(UserRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/users/all", get_container(UserRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/accounts", get_container(AccountRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/account/{account_id}", get_container(AccountRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/accounts/all", get_container(AccountRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/transactions", get_container(TransactionRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/transaction/{transaction_id}", get_container(TransactionRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/transactions/all", get_container(TransactionRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/loans", get_container(LoanRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/loan/{loan_id}", get_container(LoanRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/loans/all", get_container(LoanRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/payments", get_container(PaymentRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/payment/{payment_id}", get_container(PaymentRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/payments/all", get_container(PaymentRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/security", get_container(SecurityRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/security/{security_id}", get_container(SecurityRepository).resolve(Dependency), methods=["POST"])
# app.add_api_route("/securities/all", get_container(SecurityRepository).resolve(Dependency), methods=["POST"])
#

user_repo = UserRepository(session)
account_repo = AccountRepository(session)
payment_repo = PaymentRepository(session)
loan_repo = LoanRepository(session)
transaction_repo = TransactionRepository(session)
security_repo = SecurityRepository(session)


@app.post("/users")
async def create_user(data: UserCreate, db_session: Session = Depends(get_db)):
    return user_repo.create(data)


@app.get("/user/{user_id}")
async def get_user(user_id: int, db_session: Session = Depends(get_db)):
    return user_repo.get(user_id)


@app.get("/users/all")
async def get_users(db_session: Session = Depends(get_db)):
    return user_repo.get_all()


@app.post("/accounts")
async def create_account(data: AccountCreate, db_session: Session = Depends(get_db)):
    return account_repo.create(data)


@app.get("/account/{account_id}")
async def get_account(account_id: int, db_session: Session = Depends(get_db)):
    return account_repo.get(account_id)


@app.get("/accounts/all")
async def get_accounts(db_session: Session = Depends(get_db)):
    return account_repo.get_all()


@app.post("/payments")
async def create_payment(data: PaymentCreate, db_session: Session = Depends(get_db)):
    return payment_repo.create(data)


@app.get("/payment/{payment_id}")
async def get_payment(payment_id: int, db_session: Session = Depends(get_db)):
    return payment_repo.get(payment_id)


@app.get("/payments/all")
async def get_payments(db_session: Session = Depends(get_db)):
    return payment_repo.get_all()


@app.post("/loans")
async def create_loan(data: LoanCreate, db_session: Session = Depends(get_db)):
    return loan_repo.create(data)


@app.get("/loan/{loan_id}")
async def get_loan(loan_id: int, db_session: Session = Depends(get_db)):
    return loan_repo.get(loan_id)


@app.get("/loans/all")
async def get_loans(db_session: Session = Depends(get_db)):
    return loan_repo.get_all()


@app.post("/transactions")
async def create_transaction(data: TransactionCreate, db_session: Session = Depends(get_db)):
    return transaction_repo.create(data)


@app.get("/transaction/{transaction_id}")
async def get_transaction(transaction_id: int, db_session: Session = Depends(get_db)):
    return transaction_repo.get(transaction_id)


@app.get("/transactions/all")
async def get_transactions(db_session: Session = Depends(get_db)):
    return transaction_repo.get_all()


@app.post("/security")
async def create_security(data: SecurityCreate, db_session: Session = Depends(get_db)):
    return security_repo.create(data)


@app.get("/security/{security_id}")
async def get_security(security_id: int, db_session: Session = Depends(get_db)):
    return security_repo.get(security_id)


@app.get("/securities/all")
async def get_securities(db_session: Session = Depends(get_db)):
    return security_repo.get_all()
