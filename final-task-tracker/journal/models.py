from datetime import datetime

import sqlalchemy
from sqlalchemy import func, Column, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from journal.choices import RequestEnum
from users.models import User
from utils.model_constants import default_id


class Journal(Base):
    __tablename__ = "access_logs"

    id: Mapped[default_id]
    data = Column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    method: Mapped[str]
    request: Mapped[str]

    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))

    user = relationship(User, back_populates="logs")
