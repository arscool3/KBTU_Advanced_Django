from datetime import datetime

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from utils.model_constants import default_id


class TaskComment(Base):
    __tablename__ = "task_comment"

    id: Mapped[default_id]
    body: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    task_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("task.id"))

    user = relationship("User", back_populates="comments")
    task = relationship("Task", back_populates="comments")
