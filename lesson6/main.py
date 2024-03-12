from typing import Annotated, List

import punq
from fastapi import FastAPI, Depends
from sqlalchemy import select

import database as db
import schemas
import models
from repository import AbsRepository, UserRepository, PostRepository, CommentRepository

app = FastAPI()

# Create Web Application using FastAPI
# You need to implement
# at least 8 endpoints // I have 6 endpoints
# at least 4 models // I have 3 working models
# at least 3 relationships // I have 3 relationships - User-Post, Post-Comment, User-Comment (one to many)
# at least 1 dependency injection as class and 2 as methods // 2 dependency injection as methods


class Dependency:
    def __init__(self, repo: AbsRepository):
        self.repo = repo

    def __call__(self, id: int) -> schemas.ReturnType:
        return self.repo

    def get_list(self) -> List[schemas.ReturnType]:
        return self.repo.get_list()

    def add(self, data : schemas.CreationType):
        return self.repo.add(data)


def get_container(repository: type[AbsRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbsRepository, repository, instance=repository(session=db.session))
    container.register(Dependency)
    return container


@app.get('/users')
def get_users(users: Annotated[List[schemas.User], Depends(get_container(UserRepository).resolve(Dependency).get_list)]):
    if users is None:
        return 'No users'
    return users


@app.post('/users')
def add_users(user: Annotated[schemas.User, Depends(get_container(UserRepository).resolve(Dependency).add)]):
    if user is None:
        return 'Try again'
    return user


@app.get('/posts')
def get_users(posts: Annotated[List[schemas.Post], Depends(get_container(PostRepository).resolve(Dependency).get_list)]):
    if posts is None:
        return 'No posts'
    return posts


@app.post('/posts')
def add_users(post: Annotated[schemas.Post, Depends(get_container(PostRepository).resolve(Dependency).add)]):
    if post is None:
        return 'Try again'
    return post


@app.get('/comments')
def get_users(comments: Annotated[List[schemas.Comment], Depends(get_container(CommentRepository).resolve(Dependency).get_list)]):
    if comments is None:
        return 'No comments'
    return comments


@app.post('/comments')
def add_users(comment: Annotated[schemas.Comment, Depends(get_container(CommentRepository).resolve(Dependency).add)]):
    if comment is None:
        return 'Try again'
    return comment


# @app.get('posts')

