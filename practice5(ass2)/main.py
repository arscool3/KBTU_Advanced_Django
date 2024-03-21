from fastapi import FastAPI, Depends

app = FastAPI()


class OrderService:
    def get_order(self, order_id: int):
        return {"order_id": order_id, "items": ["Chicken", "Fries", "Coke"]}

order_service = OrderService()


def get_order_from_service(order_id: int, service: OrderService = Depends()):
    return service.get_order(order_id)

@app.get("/order/{order_id}")
async def read_order(order: dict = Depends(get_order_from_service)):
    return order


def get_total(order: dict = Depends(get_order_from_service)):
    total_price = len(order["items"]) * 5  
    return {"total_price": total_price}

@app.get("/order/{order_id}/total")
async def read_order_total(total: dict = Depends(get_total)):
    return total


class DiscountService:
    def apply_discount(self, total_price: int):
        
        return total_price * 0.9 

discount_service = DiscountService()

@app.get("/order/{order_id}/discounted_total")
async def read_discounted_total(order: dict = Depends(get_order_from_service),
                                discount_service: DiscountService = Depends()):
    total_price = len(order["items"]) * 5 
    total_price = discount_service.apply_discount(total_price)
    return {"discounted_total_price": total_price}