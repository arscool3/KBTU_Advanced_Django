from datetime import datetime

from utils.schemas_config import BaseSchema


class BaseNotification(BaseSchema):
    message: str


class CreateNotification(BaseNotification):
    user_id: int


class Notification(BaseNotification):
    id: int
    created_at: datetime
