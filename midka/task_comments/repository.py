from task_comments import schemas
from task_comments.models import TaskComment
from utils.repository import BaseRepository


class TaskCommentRepo(BaseRepository):
    model = TaskComment
    action_schema = {
        "list": schemas.TaskComment,
        "retrieve": schemas.TaskComment,
        "create": schemas.CreateTaskCommentResponse,
    }
