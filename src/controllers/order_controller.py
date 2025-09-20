from sqlalchemy.orm import Session
from src.models.user_model import Order, User, Cart, Product
from src.utils.dtos import OrderSchema
from fastapi import HTTPException

def placeOrder(body:OrderSchema,db:Session, user:User):
    cartItems = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not cartItems:
        return f"User {user.name}'s Cart is empty..."
    
    totalBill = 0.0
    orders = []

    for item in cartItems:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product id {item.product_id} not found")
        if product.in_stock < item.quantity:
            raise HTTPException(400, f"Not enough stock for product {product.name}")
        
        product.in_stock -= item.quantity
        item_price = item.quantity * product.price
        totalBill += item_price

    
        newOrder = Order(
            user_id = user.id,
            product_id = product.id,
            count = item.quantity,
            total_price = item_price,
            status = "Order placed successfully...",
            address_id=body.address_id if hasattr(body, "address_id") else None
        )  
        db.add(newOrder)
        orders.append(newOrder)
    total_products_count = sum(item.quantity for item in cartItems)
    
    db.commit()
    db.query(Cart).filter(Cart.user_id == user.id).delete()
    db.commit()

    return {
        "Status": "Order placed....",
        "Order-placed by": user.name,
        "Total-Bill":totalBill,
        "Products-count" : total_products_count,
        "orders_created":len(orders)
    }