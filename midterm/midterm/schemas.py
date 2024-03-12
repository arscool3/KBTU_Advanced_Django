from pydantic import BaseModel


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


class CreateCategory(BaseModel):
    name: str


class CreatePost(BaseModel):
    title: str
    content: str
    author_id: str
    category_id: str
