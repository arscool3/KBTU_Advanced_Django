from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class AnalysProduct(Base):
    __tablename__ = "analys_product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer)
    product_name: Mapped[str] = mapped_column(String)
    count: Mapped[int] = mapped_column(Integer)
    calculated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

