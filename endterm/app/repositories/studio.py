from app.models import Movie, Studio
from utils.repository import BaseRepository
from .. import schemas


class StudioRepo(BaseRepository):
    model = Studio
    action_schema = {
        "list": schemas.Studio,
        "retrieve": schemas.Studio,
        "create": schemas.Studio,
    }
