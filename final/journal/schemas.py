from datetime import datetime
from typing import Optional

from users.schemas import BaseUser
from utils.schemas_config import BaseSchema


class Journal(BaseSchema):
    id: int
    timestamp: datetime
    request: str
    method: str
    user: BaseUser
    data: Optional[dict]


class JournalMessage(BaseSchema):
    data: Optional[dict]
    user_id: int
    request: str
    method: str
