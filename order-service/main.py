from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

# In-memory "database" to store orders
orders_db = {}

class Order(BaseModel):
    product_id: str
    quantity: int
    user_id: str

@app.post("/create-order")
def create_order(order: Order):
    order_id = str(uuid.uuid4())
    orders_db[order_id] = {
        "order_id": order_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "user_id": order.user_id,
        "status": "pending"
    }
    # Normally, you'd call Inventory Service to reserve stock here
    return {"message": "Order created", "order_id": order_id}

@app.get("/order/{order_id}")
def get_order(order_id: str):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order