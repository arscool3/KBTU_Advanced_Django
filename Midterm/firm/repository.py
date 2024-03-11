from firm import schemas
from firm.models import Firm
from repository import BaseRepository


class FirmRepo(BaseRepository):
    model = Firm
    action_schema = {
        "list": schemas.Firm,
        "get_by_id": schemas.Firm,
        "create": schemas.CreateFirm
    }