from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from src.controllers.user_controller import SECRET_KEY, ALGORITHM, get_user_by_username
from src.db.db import get_db


def is_authenticated(
    req: Request,
    db: Session = Depends(get_db)
 ):
    token = req.headers.get("authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "You are not authorized"}
        )
    
    token = token.split(" ")[-1]  # remove "Bearer"
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token has expired"}
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token"}
        )
    
    username = data.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "You are not authorized"}
        )
    
    user = get_user_by_username(username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "You are not authorized"}
        )
    
    return user

def is_admin(req: Request, db: Session = Depends(get_db)):
    user = is_authenticated(req, db)
    
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Only Admin can perform that method"}
        )
    
    return user

def is_seller(req: Request, db: Session = Depends(get_db)):
    seller = is_authenticated(req, db)
    
    if not seller.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Only Seller can perform that method"}
        )
    
    return seller

def authorize_admin_or_seller(req: Request, db:Session = Depends(get_db)):
    user = is_authenticated(req, db)
    
    if not (user.is_admin or user.is_seller):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Access denied: Only admins or sellers can perform this action."}
        )
    
    return user