from pydantic import BaseModel


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class User(BaseUser):
    id: int


class CreateUser(BaseUser):
    pass


class BasePost(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True


class CreatePost(BasePost):
    author_id: int


class Post(BasePost):
    author: User


class BaseComment(BaseModel):
    text: str

    class Config:
        from_attributes = True


class CreateComment(BaseComment):
    user_id: int
    post_id: int


class Comment(BaseComment):
    user: User
    post: Post


class BaseLike(BaseModel):
    class Config:
        from_attributes = True


class Like(BaseLike):
    user: User
    post: Post


class CreateLike(BaseLike):
    user_id: int
    post_id: int
