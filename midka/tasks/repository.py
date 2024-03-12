from tasks import schemas
from tasks.models import Task
from utils.repository import BaseRepository


class TaskRepo(BaseRepository):
    model = Task
    action_schema = {
        "list": schemas.Task,
        "retrieve": schemas.Task,
        "create": schemas.Task,
    }
