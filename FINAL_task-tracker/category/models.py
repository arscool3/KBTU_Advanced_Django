from sqlalchemy.orm import Mapped, relationship

from database import Base
from utils.model_constants import default_id


class Category(Base):
    __tablename__ = "category"

    id: Mapped[default_id]
    title: Mapped[str]

    tasks = relationship("Task", back_populates="category")
