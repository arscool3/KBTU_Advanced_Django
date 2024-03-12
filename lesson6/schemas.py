from pydantic import BaseModel
from datetime import datetime


class BaseUser(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class User(BaseUser):
    id: int


class CreateUser(BaseUser):
    pass


class BasePost(BaseModel):
    title: str
    user_id: int
    published_at: datetime

    class Config:
        from_attributes = True


class Post(BasePost):
    id: int


class CreatePost(BasePost):
    pass


class BaseComment(BaseModel):
    text: str
    post_id: int
    user_id: int

    class Config:
        from_attributes = True


class Comment(BaseComment):
    id: int
    published_at: datetime


class CreateComment(BaseComment):
    pass


class BaseFollow(BaseModel):
    follower_id: int
    following_id: int

    class Config:
        from_attributes = True


class Follow(BaseFollow):
    id: int


class CreateFollow(BaseFollow):
    pass


ReturnType = User | Post | Comment
CreationType = CreateUser | CreatePost | CreateComment

