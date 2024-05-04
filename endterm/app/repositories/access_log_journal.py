from app import schemas
from app.models import AccessLogJournal
from utils.repository import BaseRepository


class JournalRepo(BaseRepository):
    model = AccessLogJournal
    action_schema = {
        "list": schemas.Journal,
    }