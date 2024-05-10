from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from pydantic import BaseModel
from typing import List, Optional

# Pydantic model for creating a new user
class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str

# Pydantic model for creating a new order
class OrderCreate(BaseModel):
    user_id: int
    seller_id: int
    product_id: int
    quantity: int

# Pydantic model for creating a new product
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

# Pydantic model for creating a new category
class CategoryCreate(BaseModel):
    name: str
    
class SellerCreate(BaseModel):
    name: str



# Define the database connection
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session class for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define SQLAlchemy models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    orders = relationship("Order", back_populates="user")


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    orders = relationship("Order", back_populates="seller")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    user = relationship("User", back_populates="orders")
    seller = relationship("Seller", back_populates="orders")
    product = relationship("Product")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    products = relationship("Product", back_populates="category")
