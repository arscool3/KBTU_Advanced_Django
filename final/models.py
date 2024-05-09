from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    coworkings = relationship("Coworking", back_populates="category")

class Coworking(Base):
    __tablename__ = 'coworkings'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="coworkings")
    bookings = relationship("Booking", back_populates="coworking")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # Add other user attributes as needed

    bookings = relationship("Booking", back_populates="user")
    orders = relationship("Order", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    coworking_id = Column(Integer, ForeignKey('coworkings.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    coworking = relationship("Coworking", back_populates="bookings")
    user = relationship("User", back_populates="bookings")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    # Add order details like food item, quantity, etc.
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="orders")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="payments")
