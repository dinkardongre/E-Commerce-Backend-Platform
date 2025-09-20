from sqlalchemy.orm import Session
from src.utils.dtos import CategorySchema
from src.models.user_model import User, Category
from fastapi import HTTPException, status


def createCategory(body:CategorySchema, db:Session, admin_user: User):
    existing = db.query(Category).filter(Category.name == body.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )

    new_category = Category(
        **body.model_dump(), user_id = admin_user.id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {
        "status": "Category created successfully",
        "category": {
            "id": new_category.id,
            "name": new_category.name,
            "description": new_category.description,
            "created_by": admin_user.username
        }
    }

def getAllCategories(db:Session):
    return db.query(Category).all()

def updateCategory(body:CategorySchema, db:Session, admin_user:User):
    category = db.query(Category).filter(Category.user_id == admin_user.id).first()
    if not Category:
        raise HTTPException(404, detail={"Errot r": "Category not found"})
    
    data = body.model_dump()
    for k, v in data.items():
        setattr(category, k, v)
    db.commit()
    db.refresh(category)
    return {"Status": "Category updated successfully", "UpdatedCategory": category}

def deleteCategory(db:Session, admin_user:User):
    category = db.query(Category).filter(Category.user_id == admin_user.id).first()
    if not Category:
        raise HTTPException(404, detail={"Error": "Category not found"})
    
    db.delete(category)
    db.commit()