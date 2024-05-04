from app.models import Movie
from utils.repository import BaseRepository
from .. import schemas


class MovieRepo(BaseRepository):
    model = Movie
    action_schema = {
        "list": schemas.Movie,
        "retrieve": schemas.Movie,
        "create": schemas.Movie,
    }
