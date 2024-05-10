from sqlalchemy.orm import Session
from app.models.inventory import Inventory

class InventoryService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def update_inventory(self, product_id: int, quantity: int):
        inventory_item = self.db.query(Inventory).filter(Inventory.product_id == product_id).first()
        if inventory_item:
            inventory_item.quantity += quantity
        else:
            inventory_item = Inventory(product_id=product_id, quantity=quantity)
            self.db.add(inventory_item)
        self.db.commit()
        return inventory_item
