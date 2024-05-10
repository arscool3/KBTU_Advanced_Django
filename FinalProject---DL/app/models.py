from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import date

from app.database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Book(Base):
    __tablename__ = "books"

    id: Mapped[_id]
    title: Mapped[str]
    year: Mapped[int]
    genre: Mapped[str]
    summary: Mapped[str]
    available_copies: Mapped[int]

    author_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('authors.id'))
    publisher_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('publishers.id'))

    author: Mapped['Author'] = relationship("Author", back_populates="books")
    publisher: Mapped['Publisher'] = relationship("Publisher", back_populates="books")

    loans: Mapped[list['Loan']] = relationship("Loan", back_populates="book")
    reservations: Mapped[list['Reservation']] = relationship("Reservation", back_populates="book")


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[_id]
    name: Mapped[str]
    bio: Mapped[str]

    books: Mapped[list['Book']] = relationship("Book", back_populates="author")


class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[_id]
    name: Mapped[str]
    address: Mapped[str]
    contact: Mapped[str]

    books: Mapped[list['Book']] = relationship("Book", back_populates="publisher")


class Member(Base):
    __tablename__ = "members"

    id: Mapped[_id]
    full_name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    address: Mapped[str]
    membership_date:Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())

    loans: Mapped[list['Loan']] = relationship("Loan", back_populates="member")
    reservations: Mapped[list['Reservation']] = relationship("Reservation", back_populates="member")


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[_id]
    loan_date: Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())
    status: Mapped[str]

    book_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("members.id"))

    book: Mapped[Book] = relationship("Book", back_populates="loans")
    member: Mapped[Member] = relationship("Member", back_populates="loans")


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[_id]
    reservation_date: Mapped[date] = mapped_column(sqlalchemy.Date, default=date.today())
    status: Mapped[str]

    book_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("members.id"))

    book: Mapped[Book] = relationship("Book", back_populates="reservations")
    member: Mapped[Member] = relationship("Member", back_populates="reservations")
