from datetime import datetime
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base

_id = Annotated[int, mapped_column(sa.Integer, primary_key=True)]


class User(Base):
    __tablename__ = 'users'
    id: Mapped[_id]
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped['Project'] = relationship(back_populates='user')
    posts: Mapped['Post'] = relationship(back_populates='user')
    messages: Mapped['Message'] = relationship(back_populates='sender')

    profile: Mapped['Profile'] = relationship(back_populates='user')

    contribution_id: Mapped[int] = mapped_column(sa.ForeignKey('contributions.id'))
    contribution: Mapped['Contribution'] = relationship(back_populates='users')


class Profile(Base):
    __tablename__ = 'profiles'
    id: Mapped[_id]
    education: Mapped[str] = mapped_column()
    experience: Mapped[int] = mapped_column(default=None)
    stack: Mapped[str] = mapped_column()
    current_workplace: Mapped[str] = mapped_column()
    coverletter: Mapped[str] = mapped_column()

    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'), unique=True)

    user: Mapped[User] = relationship(back_populates='profile')


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[_id]
    content: Mapped[str]

    sender_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))

    sender: Mapped[User] = relationship(back_populates='messages')


class Project(Base):
    __tablename__ = 'projects'
    id: Mapped[_id]
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    github_link: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    creator_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='projects')
    contribution: Mapped['Contribution'] = relationship(back_populates='project')


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[_id]
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    likes: Mapped[int] = mapped_column(default=0)

    author_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='posts')


class Contribution(Base):
    __tablename__ = 'posts'
    id: Mapped[_id]
    project_id: Mapped[int] = mapped_column(sa.ForeignKey('projects.id'), nullable=False)

    project: Mapped[Project] = relationship(back_populates='contribution')
    contributors: Mapped[User] = relationship(back_populates='users')