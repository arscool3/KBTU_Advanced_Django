from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from utils.model_constants import default_id


class Project(Base):
    __tablename__ = "project"

    id: Mapped[default_id]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)

    users = relationship("User", back_populates="project")
    tasks = relationship("Task", back_populates="project")
