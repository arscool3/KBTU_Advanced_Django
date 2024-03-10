from pydantic import EmailStr

from notifications.schemas import Notification
from utils.schemas_config import BaseSchema


class BaseUser(BaseSchema):
    first_name: str
    last_name: str
    email: EmailStr


class CreateUser(BaseUser):
    project_id: int


class User(BaseUser):
    id: int
    notifications: list[Notification]
