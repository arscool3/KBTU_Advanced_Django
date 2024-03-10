from datetime import date
from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True


class User(BaseUser):
    id: int
    courses: list['Course'] = []
    purchases: list['Purchase'] = []
    progress: list['Progress'] = []


class CreateUser(BaseUser):
    password: str


class BaseCourse(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        from_attributes = True


class Course(BaseCourse):
    id: int
    videos: list['Video'] = []
    reviews: list['Review'] = []


class CreateCourse(BaseCourse):
    pass


class BaseVideo(BaseModel):
    title: str
    url: str

    class Config:
        from_attributes = True


class Video(BaseVideo):
    id: int
    course_id: int


class CreateVideo(BaseVideo):
    course_id: int


class BaseReview(BaseModel):
    content: str

    class Config:
        from_attributes = True


class Review(BaseReview):
    id: int
    course_id: int
    user_id: int


class CreateReview(BaseReview):
    course_id: int
    user_id: int


class BaseProgress(BaseModel):
    completion_percentage: float

    class Config:
        from_attributes = True


class Progress(BaseProgress):
    id: int
    user_id: int
    course_id: int


class CreateProgress(BaseProgress):
    user_id: int
    course_id: int


class BasePurchase(BaseModel):
    purchase_date: date

    class Config:
        from_attributes = True


class Purchase(BasePurchase):
    id: int
    user_id: int
    course_id: int


class CreatePurchase(BasePurchase):
    user_id: int
    course_id: int
