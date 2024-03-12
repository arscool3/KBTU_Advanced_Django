import uuid
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

''' 
Models: User, Post, Favorite, Comment, Like, Category
Relationships
User one to many Post, Comment, Like
User one to one Favorite
Favorite many to many Post
Post one to many Like, Comment
Post one to one Category
'''

associations_post_favorite = Table(
    'associations_post_favorite',
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("favorite_id", ForeignKey("favorites.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    favorite: Mapped["Favorite"] = relationship("Favorite", back_populates="owner")


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
    favorites: Mapped[list["Favorite"]] = relationship(secondary=associations_post_favorite,back_populates="posts")


class Favorite(Base):
    __tablename__ = 'favorites'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="favorite")
    posts: Mapped[list["Post"]] = relationship(secondary=associations_post_favorite ,back_populates="favorites")

