from users.schemas import User, UserShort
from utils.schemas_config import BaseSchema


class BaseTaskComment(BaseSchema):
    body: str


class CreateTaskComment(BaseTaskComment):
    user_id: int
    task_id: int


class CreateTaskCommentResponse(BaseTaskComment):
    id: int
    user: UserShort


class TaskComment(BaseTaskComment):
    id: int
    user: UserShort
