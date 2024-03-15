
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy.orm import sessionmaker


url = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('authors.id'))
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'))

    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")

class Author(Base):
    __tablename__ = 'authors'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)

    books = relationship("Book", back_populates="author")

class Category(Base):
    __tablename__ = 'categories'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)

    books = relationship("Book", back_populates="category")

Session = Session(bind=engine)


# import sqlalchemy as sa

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Mapped, Session, mapped_column

# url = "postgresql://postgres:postgres@localhost/postgres"
# engine = create_engine(url)
# session = Session(engine)

# Base = declarative_base()

# class Teacher(Base):
#     __tablename__ = 'teachers'

#     id: Mapped[int] = mapped_column(sa.INT, primary_key=True)
#     name: Mapped[str]
#     yea: Mapped[int]

# class Student(Base):
#     __tablename__ = 'students'

#     id: Mapped[int] = mapped_column(sa.INT, primary_key=True)
#     name: Mapped[str]
#     age: Mapped[int]

