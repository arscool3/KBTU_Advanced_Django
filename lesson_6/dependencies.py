from typing import List

import schemas
from custom_types import ListReturnType
from repositories import AbcRepository


class PostCreateDep:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, instance: schemas.CreatePost) -> schemas.CreatePost:
        return self.repo.create(instance)


class CommentCreateDep:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, instance: schemas.CreateComment) -> schemas.CreateComment:
        return self.repo.create(instance)


class LikeCreateDep:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, instance: schemas.CreateLike) -> schemas.CreateLike:
        return self.repo.create(instance)


class ListDep:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self) -> ListReturnType:
        return self.repo.get_all()
