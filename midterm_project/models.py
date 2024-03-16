# Bank system
from typing import Annotated
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True, autoincrement=True)]


# User one --> many Account
# User one --> many Loan
# User one --> one Security
class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    name: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[str]

    __table_args__ = (
        sqlalchemy.UniqueConstraint('email'),
        sqlalchemy.UniqueConstraint('phone_number')
    )


# Account many --> one User
# Account one --> many Transactions
class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    account_number: Mapped[str]
    account_type: Mapped[str]
    balance: Mapped[float]

    user: Mapped[User] = relationship(backref='accounts')

    __table_args__ = (
        sqlalchemy.UniqueConstraint('account_number'),
    )


# Transactions many --> one Account
class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[_id]
    account_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('accounts.id'))
    transaction_type: Mapped[str]
    amount: Mapped[float]
    timestamp: Mapped[datetime]
    source: Mapped[str]
    destination: Mapped[str]

    account: Mapped[Account] = relationship(backref='transactions')


# Loan many --> one User
# Loan one --> many Payment
class Loan(Base):
    __tablename__ = 'loans'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    loan_amount: Mapped[float]
    interest_rate: Mapped[float]
    start_date: Mapped[datetime]
    term: Mapped[int]
    purpose: Mapped[str]
    late_fee: Mapped[float]

    user: Mapped[User] = relationship(backref='loans')


# Payment many --> one Loan
class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[_id]
    loan_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('loans.id'))
    payment_amount: Mapped[float]
    payment_date: Mapped[datetime]

    loan: Mapped[Loan] = relationship(backref='payments')


# Security one --> one User
class Security(Base):
    __tablename__ = 'securities'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    username: Mapped[str]
    password: Mapped[str]

    user: Mapped[User] = relationship(backref='security', uselist=False)

    __table_args__ = (
        sqlalchemy.UniqueConstraint('username'),
    )
