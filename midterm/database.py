import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

url = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)
    supplier_id = sa.Column(sa.Integer, sa.ForeignKey('suppliers.id'))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'))

    supplier = relationship("Supplier", back_populates="products")
    category = relationship("Category", back_populates="products")

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)

    products = relationship("Product", back_populates="supplier")

class Category(Base):
    __tablename__ = 'categories'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)

    products = relationship("Product", back_populates="category")
