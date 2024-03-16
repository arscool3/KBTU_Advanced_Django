from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from models import User, Account, Transaction, Loan, Payment, Security


class BaseRepository(ABC):
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def get(self, item_id):
        pass

    def get_all(self):
        pass


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data):
        db_user = User(**data.model_dump())
        self.session.add(db_user)
        self.session.commit()
        self.session.close()
        return "User was added"

    def get(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_all(self):
        return self.session.query(User).all()


class AccountRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data):
        db_account = Account(**data.model_dump())
        self.session.add(db_account)
        self.session.commit()
        self.session.close()
        return "Account was added"

    def get(self, account_id):
        return self.session.query(Account).filter(Account.id == account_id).first()

    def get_all(self):
        return self.session.query(Account).all()


class TransactionRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data):
        db_transaction = Transaction(**data.model_dump())
        self.session.add(db_transaction)
        self.session.commit()
        self.session.close()
        return "Transaction was added"

    def get(self, transaction_id):
        return self.session.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_all(self):
        return self.session.query(Transaction).all()


class LoanRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data):
        db_loan = Loan(**data.model_dump())
        self.session.add(db_loan)
        self.session.commit()
        self.session.close()
        return "Loan was added"

    def get(self, loan_id):
        return self.session.query(Loan).filter(Loan.id == loan_id).first()

    def get_all(self):
        return self.session.query(Loan).all()


class PaymentRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data):
        db_payment = Payment(**data.model_dump())
        self.session.add(db_payment)
        self.session.commit()
        self.session.close()
        return "Payment was added"

    def get(self, payment_id):
        return self.session.query(Payment).filter(Payment.id == payment_id).first()

    def get_all(self):
        return self.session.query(Payment).all()


class SecurityRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data):
        db_security = Security(**data.model_dump())
        self.session.add(db_security)
        self.session.commit()
        self.session.close()
        return "Security was added"

    def get(self, security_id):
        return self.session.query(Security).filter(Security.id == security_id).first()

    def get_all(self):
        return self.session.query(Security).all()
