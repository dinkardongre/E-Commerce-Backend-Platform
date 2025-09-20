from sqlalchemy.orm import Session
from src.models.user_model import Cart, User
from src.utils.dtos import CartSchema
from fastapi import HTTPException

def addCart(body:CartSchema, db:Session, user:User):
    if not user.is_active:
        raise HTTPException(401, detail=f"User {user.name} is not active...")
    item = Cart(**body.model_dump(), user_id = user.id)
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "Status": f"Item added to cart of {user.name}",
        "cart-details":item
    }

def getAllCartItems(db:Session, user:User):
    items = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not items:
        raise HTTPException(404, detail="Cart is empty...")
    return {
        "User": user.username,
        "Cart":items
    }


def updateCartItem(cart_id:int,body:CartSchema, db:Session, user:User):
    item = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not item:
        raise HTTPException(404, detail="Cart is empty...")
    updateItem = db.query(Cart).filter(Cart.id == cart_id).first()
    data = body.model_dump()
    for k,v in data.items():
        setattr(updateItem, k, v)
    db.commit()
    db.refresh(updateItem)

    return {
        "Status": "Cart_item updated...",
        "update-cart-product":updateItem
    }

def deleteCartItem(cart_id:int,db:Session, user:User):
    item = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not item:
        raise HTTPException(404, detail="Cart is empty...")
    deletedItem = db.query(Cart).filter(Cart.id == cart_id).first()
    db.delete(deletedItem)
    db.commit()
    return {
        "Status": "Cart_item deleted...",
        "deleted-cart-product":deletedItem
    }