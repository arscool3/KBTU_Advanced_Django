from datetime import datetime

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from utils.model_constants import default_id


class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[default_id]
    message: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))

    user = relationship("User", back_populates="notifications")
