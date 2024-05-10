import dramatiq

@dramatiq.actor
def generate_sales_reports():
    from ..db.session import SessionLocal
    from ..models import Order

    db = SessionLocal()
    try:
        order_count = db.query(Order).count()
        print(f"Total orders: {order_count}")
    finally:
        db.close()
