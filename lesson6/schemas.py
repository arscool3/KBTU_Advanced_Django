from pydantic import BaseModel


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

    class Config:
        from_attributes = True


class Post(BasePost):
    id: int


class CreatePost(BasePost):
    pass

