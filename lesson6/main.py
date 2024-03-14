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

    def __call__(self):
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
    return 'No comments' if users is None else users


@app.post('/users')
def add_users(user: schemas.CreateUser,
              repo: UserRepository = Depends(get_container(UserRepository).resolve(Dependency))):
    return 'Try again' if user is None else repo.add(data=user)


@app.get('/posts')
def get_posts(posts: Annotated[List[schemas.Post], Depends(get_container(PostRepository).resolve(Dependency).get_list)]):
    return 'No comments' if posts is None else posts


@app.post('/posts')
def add_post(post: schemas.CreatePost,
             repo: PostRepository = Depends(get_container(PostRepository).resolve(Dependency))):
    return 'Try again' if post is None else repo.add(data=post)


@app.get('/comments')
def get_comments(comments: Annotated[List[schemas.Comment], Depends(get_container(CommentRepository).resolve(Dependency).get_list)]):
    return 'No comments' if comments is None else comments


@app.post('/comments')
def add_comment(comment: schemas.CreateComment,
                repo: CommentRepository = Depends(get_container(CommentRepository).resolve(Dependency))):
    return 'Try again' if comment is None else repo.add(data=comment)

