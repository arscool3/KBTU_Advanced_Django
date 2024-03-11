import uuid
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


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str] = mapped_column(nullable=False)

