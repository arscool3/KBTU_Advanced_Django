from users.schemas import User
from utils.schemas_config import BaseSchema


class BaseTaskComment(BaseSchema):
    body: str


class CreateTaskComment(BaseTaskComment):
    user_id: int
    task_id: int


class TaskComment(BaseTaskComment):
    id: int
    user: User
