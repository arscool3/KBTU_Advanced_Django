from typing import Annotated

import punq
from fastapi import FastAPI, Depends
from sqlalchemy import select

import database as db
import schemas
import models
from repository import AbsRepository, UserRepository

app = FastAPI()

# Create Web Application using FastAPI
# You need to implement
# at least 8 endpoints // I have 6 endpoints
# at least 4 models // I have 3 working models
# at least 3 relationships // I have 3 relationships - User-Post, Post-Comment, User-Comment (one to many)
# at least 1 dependency injection as class and 2 as methods // Not implemented yet


class Dependency:
    def __init__(self, repo: AbsRepository):
        self.repo = repo

    def get_list(self):
        self.repo.get_list()


def get_container(repository: type[AbsRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbsRepository, repository, instance=repository(session=db.session))
    container.register(Dependency)
    return container

# trying to use DI

# @app.get('/users')
# def get_users(users: Annotated[list[schemas.User], Depends(get_container(UserRepository).resolve(Dependency).get_list)]) -> list[schemas.User]:
#     return users


@app.get('/users')
def get_users():
    db_users = db.session.execute(select(models.User)).scalars().all()
    users = []
    for user in db_users:
        users.append(user)
    return users


@app.post('/users')
def add_users(user: schemas.CreateUser):
    db.session.add(models.User(**user.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{user.name} was added"


@app.get('/posts')
def get_posts():
    db_posts = db.session.execute(select(models.Post)).scalars().all()
    posts = []
    for post in db_posts:
        posts.append(post)
    return posts


@app.post('/posts')
def add_post(post: schemas.CreatePost):
    db.session.add(models.Post(**post.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{post.title} was published"


@app.get('/comments')
def get_comments():
    db_comments = db.session.execute(select(models.Comment)).scalars().all()
    comments = []
    for comment in db_comments:
        comments.append(comment)
    return comments


@app.post('/comments')
def add_comment(comment: schemas.CreateComment):
    db.session.add(models.Comment(**comment.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{comment.text} was published"
