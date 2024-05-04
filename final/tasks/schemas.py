from typing import Optional, List

from category.schemas import Category
from projects.schemas import Project
from task_comments.schemas import TaskComment
from users.schemas import UserShort
from utils.schemas_config import BaseSchema


class BaseTask(BaseSchema):
    title: str
    description: Optional[str]
    status: str


class CreateTask(BaseTask):
    user_id: int
    category_id: int
    project_id: int


class Task(BaseTask):
    id: int
    user: UserShort
    category: Category
    comments: List[TaskComment]
    project: Project
