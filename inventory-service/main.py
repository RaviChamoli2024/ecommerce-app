from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory "database" for inventory stock levels
inventory_db = {
    "dress_1": 50,
    "dress_2": 20,
    "dress_3": 30
}

class ReserveStock(BaseModel):
    product_id: str
    quantity: int

@app.post("/reserve-stock")
def reserve_stock(reservation: ReserveStock):
    product_id = reservation.product_id
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Product not found")
    if inventory_db[product_id] < reservation.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    inventory_db[product_id] -= reservation.quantity
    return {"message": "Stock reserved", "product_id": product_id, "remaining_stock": inventory_db[product_id]}

@app.get("/stock/{product_id}")
def check_stock(product_id: str):
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product_id, "stock": inventory_db[product_id]}