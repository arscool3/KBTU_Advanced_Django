from journal import schemas
from journal.models import Journal
from utils.repository import BaseRepository


class JournalRepo(BaseRepository):
    model = Journal
    action_schema = {
        "list": schemas.Journal,
    }
