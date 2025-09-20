from sqlalchemy.orm import Session
from src.utils.dtos import AddressSchema
from src.models.user_model import Address, User
from fastapi import HTTPException

def addAddress(body:AddressSchema, db:Session, user:User):
    newAddress = Address(**body.model_dump(), user_id = user.id)
    db.add(newAddress)
    db.commit()
    db.refresh(newAddress)

    return {
        "Status":f"New Address added successfully for {user.name}",
        "New-address-details":newAddress
    }

def updateAddress(body:AddressSchema, db:Session, user:User):
    address = db.query(Address).filter(Address.user_id == user.id).first()
    if not address:
        raise HTTPException(404, detail="Address not found")
    
    data = body.model_dump()
    for k,v in data.items():
        setattr(address, k, v)

    db.commit()
    db.refresh(address)

    return {
        "Status":"address is updated...",
        "updated-address":address
    }

def deleteAddress(db:Session, user:User):
    address = db.query(Address).filter(Address.user_id == user.id).first()
    if not address:
        raise HTTPException(404, detail="Address not found")
    db.delete(address)
    db.commit()

    return {
        "Status":"address is deleted...",
        "deleted-address":address
    }

def getAllUsersAddress(db:Session, user:User):
    if not user.is_admin:
        raise HTTPException(403, detail="You are not authorized for this action...")
    return db.query(Address).all()
