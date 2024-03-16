import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Table

url = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


film_actor_association = Table('film_actor_association', Base.metadata,
                               Column('film_id', Integer, ForeignKey('films.id')),
                               Column('actor_id', Integer, ForeignKey('actors.id'))
                               )

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    mail = Column(String)

    likes = relationship("Likes", back_populates="user")


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    films = relationship("Film", back_populates="genre")


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)

    films = relationship("Film", secondary=film_actor_association, back_populates="actors")


class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)

    films = relationship("Film", back_populates="director")


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    duration = Column(Integer)
    year = Column(Integer)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    director_id = Column(Integer, ForeignKey('directors.id'))

    genre = relationship("Genre", back_populates="films")
    director = relationship("Director", back_populates="films")
    actors = relationship("Actor", secondary=film_actor_association, back_populates="films")
    likes = relationship("Likes", back_populates="film")


class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    film_id = Column(Integer, ForeignKey('films.id'))

    user = relationship("User", back_populates="likes")
    film = relationship("Film", back_populates="likes")