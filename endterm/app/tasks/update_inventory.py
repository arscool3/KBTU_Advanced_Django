import dramatiq
from dramatiq.brokers.redis import RedisBroker

redis_broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(redis_broker)

@dramatiq.actor
def update_inventory(product_id, change_in_quantity):
    from ..db.session import SessionLocal
    from ..services.inventory_service import InventoryService

    db = SessionLocal()
    try:
        inventory_service = InventoryService(db)
        inventory_service.update_inventory(product_id, change_in_quantity)
    finally:
        db.close()
