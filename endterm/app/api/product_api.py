from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas import ProductCreate, ProductOut
from ..services.product_service import ProductService

router = APIRouter()

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.create_product(product)

@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    db_product = product_service.get_product_by_id(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
