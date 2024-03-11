from user import schemas
from user.models import User
from repository import BaseRepository


class UserRepo(BaseRepository):
    model = User
    action_schema = {
        "list": schemas.User,
        "get_by_id": schemas.User,
        "create": schemas.CreateUser
    }
