from sqlalchemy import Column, Integer, ForeignKey, Integer
from sqlalchemy.orm import relationship
from . import Base

class Inventory(Base):
    __tablename__ = 'inventory'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer, default=0)

    product = relationship("Product", back_populates="inventory")