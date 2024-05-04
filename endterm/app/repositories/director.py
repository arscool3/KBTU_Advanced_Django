from app.models import Movie, Director
from utils.repository import BaseRepository
from .. import schemas

class DirectorRepo(BaseRepository):
    model = Director
    action_schema = {
        "list": schemas.Director,
        "retrieve": schemas.Director,
        "create": schemas.Director,
    }