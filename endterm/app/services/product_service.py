from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

class ProductService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_product(self, product: ProductCreate):
        db_product = Product(name=product.name, description=product.description, price=product.price)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_product_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()
