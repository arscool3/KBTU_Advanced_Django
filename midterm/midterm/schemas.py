from pydantic import BaseModel, Field


class User(BaseModel):
    class Config:
        from_attributes = True

    id: str
    username: str
    first_name: str
    last_name: str


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str


class GetFavorite(BaseModel):
    class Config:
        from_attributes = True

    id: str
    owner_id: str


class Category(BaseModel):
    class Config:
        from_attributes = True

    id: str
    name: str


class CreateCategory(BaseModel):
    name: str


class CreatePost(BaseModel):
    title: str
    content: str
    author_id: str
    category_id: str


class CreateComments(BaseModel):
    body: str
    owner_id: str
    post_id: str


class Comments(BaseModel):

    class Config:
        from_attributes = True

    id: str
    body: str
    owner_id: str
    post_id: str


class GetPost(BaseModel):
    class Config:
        from_attributes = True

    id: str
    title: str
    content: str
    comments: list[Comments]
    like: list["Like"]
    category_id: str
    author_id: str


class Like(BaseModel):
    class Config:
        from_attributes = True

    id: str
    owner_id: str
    post_id: str


class CreateLike(BaseModel):
    owner_id: str = Field(...)
    post_id: str = Field(...)
