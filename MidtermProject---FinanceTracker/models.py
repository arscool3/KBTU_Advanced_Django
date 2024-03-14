from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[_id]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    accounts: Mapped[list['Account']] = relationship("Account", back_populates="owner")
    budgets: Mapped[list['Budget']] = relationship("Budget", back_populates="users")
    expenses: Mapped[list['Expense']] = relationship("Expense", back_populates="users")


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    account_name: Mapped[str]
    account_type: Mapped[str]

    owner: Mapped[User] = relationship("User", back_populates="accounts")
    transactions: Mapped[list['Transaction']] = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[_id]
    account_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('accounts.id'))
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('categories.id'))
    amount: Mapped[float]
    description: Mapped[str]
    transaction_date: Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())

    account: Mapped[Account] = relationship("Account", back_populates="transactions")
    category: Mapped['Category'] = relationship("Category", back_populates="transactions")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[_id]
    category_name: Mapped[str]

    transactions: Mapped[list[Transaction]] = relationship("Transaction", back_populates="category")
    budgets: Mapped[list['Budget']] = relationship("Budget", back_populates="category")


class Budget(Base):
    __tablename__ = 'budgets'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('categories.id'))
    amount: Mapped[float]
    added_date: Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())

    user: Mapped[User] = relationship("User", back_populates="budgets")
    category: Mapped[Category] = relationship("Category", back_populates="budgets")


class Expense(Base):
    __tablename__ = 'expenses'

    id: Mapped[_id]
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('users.id'))
    account_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('accounts.id'))
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('categories.id'))
    amount: Mapped[float]
    description: Mapped[str]
    expense_date: Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())

    user: Mapped[User] = relationship("User", back_populates="expenses")
