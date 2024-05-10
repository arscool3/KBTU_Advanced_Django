from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas import InventoryOut
from ..services.inventory_service import InventoryService

router = APIRouter()

@router.get("/{product_id}", response_model=InventoryOut)
def read_inventory(product_id: int, db: Session = Depends(get_db)):
    inventory_service = InventoryService(db)
    inventory = inventory_service.get_inventory_by_product_id(product_id)
    return inventory
