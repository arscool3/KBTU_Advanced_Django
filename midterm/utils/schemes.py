from typing import List

from pydantic import BaseModel


class BasePerson(BaseModel):
    id: int
    name: str
    username: str
    surname: str
    password: str

    class Config:
        from_attributes = True


class User(BasePerson):
    posts: list['Post']
    comments: list['Comment']
    complaints: list['Complaint']
    likes: list['Like']


class CreateUser(BaseModel):
    name: str
    surname: str
    username: str
    password: str


class LogUser(BaseModel):
    username: str
    password: str


class Admin(BasePerson):
    pass


class BaseCart(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Post(BaseCart):
    id: int
    title: str
    description: str
    # user: User
    user_id: int
    # comments: list['Comment']
    # complaints: list['Complaint']
    # likes: list['Like']


class PrevCreatePost(BaseModel):
    title: str
    description: str


class CreatePost(PrevCreatePost):
    title: str
    description: str
    user_id: int


class Comment(BaseCart):
    description: str
    # user: User
    # post: Post
    user_id: int
    post_id: int


class PrevCreateComment(BaseModel):
    description: str


class CreateComment(PrevCreateComment):
    user_id: int
    post_id: int


class Complaint(BaseCart):
    description: str
    # user: User
    # post: Post
    user_id: int
    post_id: int

class PrevCreateComplaint(BaseModel):
    description: str
class CreateComplaint(PrevCreateComplaint):
    description: str
    user_id: int
    post_id: int


class Like(BaseCart):
    pass
    # user: User
    # post: Post
    user_id: int
    post_id: int

class CreateLike(BaseModel):
    user_id: int
    post_id: int
