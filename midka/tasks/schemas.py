from typing import Optional, List

from category.schemas import Category
from task_comments.schemas import TaskComment
from tasks import choices
from users.schemas import User
from utils.schemas_config import BaseSchema


class BaseTask(BaseSchema):
    title: str
    description: Optional[str]
    status: Optional[choices.StatusEnum]


class CreateTask(BaseTask):
    user_id: int
    category_id: int
    project_id: int


class Task(BaseTask):
    id: int
    user: User
    category: Category
    comments: List[TaskComment]


