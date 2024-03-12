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
    favorite: Mapped["Favorite"] = relationship("Favorite", back_populates="owner", uselist=False)
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="owner")
    like: Mapped[list["Like"]] = relationship("Like", back_populates="owner")


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
    favorites: Mapped[list["Favorite"]] = relationship(secondary=associations_post_favorite, back_populates="posts")
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    like: Mapped[list["Like"]] = relationship("Like", back_populates="post")


class Favorite(Base):
    __tablename__ = 'favorites'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="favorite", uselist=False)
    posts: Mapped[list["Post"]] = relationship(secondary=associations_post_favorite, back_populates="favorites")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="category")


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    body: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="comments")
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Like(Base):
    __tablename__ = 'like'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="like")
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="like")
