from sqlalchemy.orm import Session

from app.publishers import schemas
from app.models import Publisher
from app.utils.repository import BaseRepository


class PublisherRepo(BaseRepository):
    model = Publisher
    session = Session
    schema = schemas.Publisher
