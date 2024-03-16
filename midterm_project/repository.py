from abc import ABC, abstractmethod

from models import User, Account, Transaction, Loan, Payment, Security


class BaseRepository(ABC):
    def __init__(self, db_session):
        self.db_session = db_session

    @abstractmethod
    def create(self, db_session, data):
        pass

    @abstractmethod
    def get(self, db_session, item_id):
        pass

    def get_all(self, db_session):
        pass


class UserRepository(BaseRepository):
    def create(self, db_session, data):
        db_user = User(**data.model_dump())
        db_session.add(db_user)
        db_session.commit()
        db_session.close()
        return "User was added"

    def get(self, db_session, user_id):
        return db_session.query(User).filter(User.id == user_id).first()

    def get_all(self, db_session):
        return db_session.query(User).all()


class AccountRepository(BaseRepository):
    def create(self, db_session, data):
        db_account = Account(**data.model_dump())
        db_session.add(db_account)
        db_session.commit()
        db_session.close()
        return "Account was added"

    def get(self, db_session, account_id):
        return db_session.query(Account).filter(Account.id == account_id).first()

    def get_all(self, db_session):
        return db_session.query(Account).all()


class TransactionRepository(BaseRepository):
    def create(self, db_session, data):
        db_transaction = Transaction(**data.model_dump())
        db_session.add(db_transaction)
        db_session.commit()
        db_session.close()
        return "Transaction was added"

    def get(self, db_session, transaction_id):
        return db_session.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_all(self, db_session):
        return db_session.query(Transaction).all()


class LoanRepository(BaseRepository):
    def create(self, db_session, data):
        db_loan = Loan(**data.model_dump())
        db_session.add(db_loan)
        db_session.commit()
        db_session.close()
        return "Loan was added"

    def get(self, db_session, loan_id):
        return db_session.query(Loan).filter(Loan.id == loan_id).first()

    def get_all(self, db_session):
        return db_session.query(Loan).all()


class PaymentRepository(BaseRepository):
    def create(self, db_session, data):
        db_payment = Payment(**data.model_dump())
        db_session.add(db_payment)
        db_session.commit()
        db_session.close()
        return "Payment was added"

    def get(self, db_session, payment_id):
        return db_session.query(Payment).filter(Payment.id == payment_id).first()

    def get_all(self, db_session):
        return db_session.query(Payment).all()


class SecurityRepository(BaseRepository):
    def create(self, db_session, data):
        db_security = Security(**data.model_dump())
        db_session.add(db_security)
        db_session.commit()
        db_session.close()
        return "Security was added"

    def get(self, db_session, security_id):
        return db_session.query(Security).filter(Security.id == security_id).first()

    def get_all(self, db_session):
        return db_session.query(Security).all()
