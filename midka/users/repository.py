from users import schemas
from users.models import User
from utils.repository import BaseRepository


class UserRepo(BaseRepository):
    model = User
    action_schema = {
        "list": schemas.User,
        "retrieve": schemas.User,
        "create": schemas.CreateUserResponse,
    }
