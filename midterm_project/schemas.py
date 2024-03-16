from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class UserCreate(Base):
    name: str
    email: str
    phone_number: str


class AccountCreate(Base):
    account_number: int
    account_type: str
    balance: float
    user_id: int


class TransactionCreate(Base):
    transaction_type: str
    amount: float
    timestamp: datetime
    source: str
    destination: str
    account_id: int


class LoanCreate(Base):
    loan_amount: int
    interest_rate: float
    start_date: datetime
    term: int
    purpose: str
    late_fee: float
    user_id: int


class PaymentCreate(Base):
    payment_amount: float
    payment_date: datetime
    loan_id: int


class SecurityCreate(Base):
    username: str
    password: str
    user_id: int
