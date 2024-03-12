from typing import Optional, List

from users.schemas import User
from utils.schemas_config import BaseSchema


class BaseProject(BaseSchema):
    name: str
    description: Optional[str]


class CreateProject(BaseProject):
    pass


class CreateProjectResponse(BaseProject):
    id: int


class Project(BaseProject):
    id: int
    users: List[User]
