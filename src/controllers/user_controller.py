import jwt as pyjwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.utils.dtos import UserSchema, LoginSchema
from src.models.user_model import User
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "29fda3b6bb9548ffada7be82af6a76598ef0bd31f348cf7f2bbbd1d4bfceed0f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(username:str,database:Session):
    user = database.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user

def register(body:UserSchema, database:Session):
    currentUser = get_user_by_username(body.username, database)
    if currentUser:
        raise HTTPException(409, detail={"Error":"User already exist"})
    
    hp = get_password_hash(body.password)

    user = User(
        name=body.name,
        email=body.email,
        mobile=body.mobile,
        username=body.username,
        hash_password=hp,
        is_admin=body.is_admin,
        is_seller=body.is_seller,
        is_active=body.is_active,
    )

    database.add(user)
    database.commit()
    database.refresh(user)

    return {
        "status":"User created successfully...",
        "user":user
    }

def login(body:LoginSchema, database:Session):
    currentUser = get_user_by_username(body.username, database)
    if not currentUser:
        raise HTTPException(404, detail={"Error":"User not found"})

    verifyPassword = verify_password(body.password, currentUser.hash_password)

    if not verifyPassword:
        raise HTTPException(404, detail="Password is incorrect")

    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    token = pyjwt.encode({"username":currentUser.username, "exp":expire}, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "Message":"Login Successfully....",
        "token":token
}

def fetchMyProfile(user:User):
    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile":user.mobile,
            "username": user.username,
        },
        "categories": user.categories,
        "products":user.products,
        "address":user.address,
        "cart":user.carts,
        "orders":user.orders
    }

def updateUser(body:UserSchema, db:Session, user:User):
    user = db.query(User).filter(User.id == user.id).first()
    if not user:
        raise HTTPException(404, detail={"Error": "User not found"})
    data = body.model_dump()
    for k, v in data.items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return {"Status": "User updated successfully", "UpdatedUser": user}


def deleteUser(db: Session, user:User):
    user = db.query(User).filter(User.id == user.id).first()
    if not user:
        raise HTTPException(404, detail={"Error": "User not found"})
    db.delete(user)
    db.commit()
    return {"Message": "User deleted", "DeletedUser": user}

def getAllUsers(db:Session, user:User):
    user = db.query(User).filter(User.id == user.id)
    if not user:
        raise HTTPException(404, detail={"Error":"You are not authorized"})
    return db.query(User).all()




def updateUserByAdmin(user_id:int, body:UserSchema, db:Session, current_user:User):

    user_to_update = db.query(User).filter(User.id == user_id).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")

    # Admin can update any non-admin user (except other admins)
    if current_user.is_admin:
        if user_to_update.is_admin and user_to_update.id != current_user.id:
            raise HTTPException(status_code=403, detail="Cannot update another admin")
    else:
        # Sellers and normal users can only update their own profile
        if user_to_update.id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this user")

    data = body.model_dump()
    for key, value in data.items():
        setattr(user_to_update, key, value)

    db.commit()
    db.refresh(user_to_update)

    return {"status": f"User updated by admin {current_user.username}", "updated_user": user_to_update}

def deleteUserByAdmin(user_id:int, db:Session, current_user:User):

    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(404, detail="User is not found")
    
    if not current_user.is_admin:
        raise HTTPException(403, detail="Not authorized to update this user")


    # if current_user.id != user_to_delete.id:
    #         raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    db.delete(user_to_delete)
    db.refresh()

    return {"Status": f"User deleted by admin...{current_user.username}",
            "deleted_user":user_to_delete }