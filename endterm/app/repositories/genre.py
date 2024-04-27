from app.models import Genre as GenreModel
from app.schemas import Genre, CreateGenre
from utils.repository import BaseRepository


class GenreRepo(BaseRepository):
    model = GenreModel
    action_schema = {
        "list": Genre,
        "retrieve": Genre,
        "create": Genre
    }