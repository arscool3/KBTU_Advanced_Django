from abc import abstractmethod
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models
from custom_types import CreateType, ListReturnType


class AbcRepository:

    @abstractmethod
    def get_all(self) -> ListReturnType:
        raise NotImplementedError()

    @abstractmethod
    def create(self, instance: CreateType) -> CreateType:
        raise NotImplementedError()


class PostRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[schemas.Post]:
        posts = self.session.execute(select(models.Post)).scalars().all()
        return [schemas.Post.model_validate(post) for post in posts]

    def create(self, post: schemas.CreatePost) -> schemas.CreatePost:
        self.session.add(models.Post(**post.model_dump()))
        self.session.commit()
        return post


class CommentRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[schemas.Comment]:
        comments = self.session.execute(select(models.Comment)).scalars().all()
        return [schemas.Comment.model_validate(comment) for comment in comments]

    def create(self, comment: schemas.CreateComment) -> schemas.CreateComment:
        self.session.add(models.Post(**comment.model_dump()))
        self.session.commit()
        return comment


class LikeRepository(AbcRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[schemas.Like]:
        likes = self.session.execute(select(models.Like)).scalars().all()
        return [schemas.Like.model_validate(like) for like in likes]

    def create(self, like: schemas.CreateLike) -> schemas.CreateLike:
        self.session.add(models.Like(**like.model_dump()))
        self.session.commit()
        return like
