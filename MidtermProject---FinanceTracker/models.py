from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from datetime import datetime

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    accounts: Mapped[list['Account']] = relationship("Account", back_populates="owner")
    budgets = relationship("Budget", back_populates="user")
    expenses = relationship("Expense", back_populates="user")


class Account(Base):
    __tablename__ = 'accounts'

    id = Mapped[_id]
    user_id = Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    account_name = Mapped[str]
    account_type = Mapped[str]

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[_id]
    account_id: Mapped[int] = relationship(sqlalchemy.ForeignKey('accounts.id'))
    category_id: Mapped[int] = relationship(sqlalchemy.ForeignKey('categories.id'))
    amount: Mapped[float]
    description: Mapped[str]
    transaction_date = Column(DateTime, default=datetime.now)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)

    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")


class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    amount = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")


class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    amount = Column(Float)
    description = Column(String, nullable=True)
    expense_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="expenses")
