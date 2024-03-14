from abc import abstractmethod
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
import schemas
import models


class AbsRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_list(self) -> List[schemas.ReturnType]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, data: schemas.CreationType):
        raise NotImplementedError()


class UserRepository(AbsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_list(self) -> List[schemas.User]:
        db_users = self.session.execute(select(models.User)).scalars().all()
        users = []
        for db_user in db_users:
            users.append(schemas.User.model_validate(db_user))
        return users

    def add(self, data: schemas.CreateUser):
        self.session.add(models.User(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return "Added user is {data}"


class PostRepository(AbsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_list(self) -> List[schemas.Post]:
        db_posts = self.session.execute(select(models.Post)).scalars().all()
        return [schemas.Post.model_validate(db_post) for db_post in db_posts]

    def add(self, data: schemas.CreatePost):
        self.session.add(models.Post(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return f"Added post is {data}"


class CommentRepository(AbsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_list(self) -> List[schemas.Comment]:
        db_comments = self.session.execute(select(models.Comment)).scalars().all()
        return [schemas.Comment.model_validate(db_comment) for db_comment in db_comments]

    def add(self, data: schemas.CreateComment):
        self.session.add(models.Comment(**data.model_dump()))
        self.session.commit()
        self.session.close()
        return f"Added comment is {data}"


class ProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_posts(self, id: int) -> List[schemas.Post]:
        db_posts = self.session.execute(select(models.Post)).scalars().all()
        user = db_citizen = self.session.get(models.User, id)
        user_posts = user.posts
        print(len(user_posts))
        return [schemas.Post.model_validate(db_post) for db_post in user_posts]

