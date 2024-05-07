from sqlalchemy import select, insert
from fastapi import FastAPI
from pydantic import BaseModel
import database as db
import core.schemas as sch
import core.models as mdl
from fastapi import HTTPException

app = FastAPI()


@app.post("/products")
def add_product(product: sch.Product) -> str:
    db.session.add(mdl.Product(**product.model_dump()))
    db.session.commit()
    db.session.close()
    return "Products was added"


@app.get("/products")
def get_products():
    db_products = db.session.execute(
            select(mdl.Product)
        ).scalars().all()
    print(db_products)
    products = []
    for product in db_products:
        products.append(sch.Product.model_validate(product))
    return products

@app.post("/customers")
def create_Customer(customer: sch.Customer) -> str:
    db.session.add(mdl.Customer(**customer.model_dump()))
    db.session.commit()
    db.session.close()
    return "Customer was added"

@app.get("/customers")
def get_customers():
    db_customers = db.session.execute(
            select(mdl.Customer)
        ).scalars().all()
   
    customers = []
    for customer in db_customers:
        customers.append(sch.Customer.model_validate(customer))
    return customers

@app.post("/createcart")
def create_Cart_for_Customer(cart: sch.Cart) -> str:
    db.session.add(mdl.Cart(**cart.model_dump()))
    db.session.commit()
    db.session.close()
    return "Cart was added"

@app.post("/addtocart")
def add_to_cart(cartitem: sch.CartItem)-> str:
    db.session.add(mdl.CartItem(**cartitem.model_dump()))
    db.session.commit()
    db.session.close()
    return "add succes"

@app.get("/cartitems")
def get_cartitems():
    db_cartitems = db.session.execute(
            select(mdl.CartItem)
        ).scalars().all()
   
    cartitems = []
    for cartitem in db_cartitems:
        cartitems.append(sch.CartItem.model_validate(cartitem))
    return cartitems


@app.get("/cartitems/{customer_id}")
def get_cartitems_for_customer(customer_id: int):
    customer = db.session.query(mdl.Customer).filter(mdl.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    cartitems = db.session.query(mdl.CartItem).join(mdl.Cart).filter(mdl.Cart.customer_id == customer_id).all()

    validated_cartitems = []
    for cartitem in cartitems:
        validated_cartitems.append(sch.CartItem.model_validate(cartitem))
    return validated_cartitems