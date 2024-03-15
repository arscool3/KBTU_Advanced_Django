from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    tt: str
    age: int
    password: str


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


class CommentCreate(BaseModel):
    content: str
    user_id: int
    post_id: int


class CategoryCreate(BaseModel):
    name: str
