from src.models.user_model import Product, User, Category
from src.utils.dtos import ProductSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request

def createProduct(body:ProductSchema, db:Session, user: User):
    new_product = Product(**body.model_dump(), user_id = user.id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "Status":"Product is created...",
        "Product-Details":new_product
    }

# def getllProducts(db:Session):
#     return db.query(Product).all()

# def getProductByCategoryId(cat_id:int, db:Session):
#     products =  db.query(Product).filter(Product.category_id == cat_id).all()
#     if not products:
#         raise HTTPException(404, detail="No Such Category found !")
#     return products

# def getProductsByName(cat_name:str, db:Session):
#     category = db.query(Category).filter(Category.name == cat_name).first()
#     if not category:
#         raise HTTPException(404, detail="No Such Category found !")

#     products = db.query(Product).filter(Product.category_id == category.id).all()
    
#     return products

def getProducts(req:Request, db:Session):
    count = req.query_params.get("count")
    minPrice = req.query_params.get("minPrice")
    maxPrice = req.query_params.get("maxPrice")
    category = req.query_params.get("category")

    products = db.query(Product)


    if category:
        category = db.query(Category).filter(Category.name == category).first()
        if not category:
            raise HTTPException(404, detail="No Such Category found !")
        products = products.filter(Product.category_id == category.id)
    if minPrice:
        products = products.filter(Product.price >= int(minPrice))
    if maxPrice:
        products = products.filter(Product.price <= int(maxPrice))
    if count:
        products = products.filter(Product.in_stock >= int(count))
    if not products:
            return "No such products found..."
    productList = products.all()
    return {
        "Products":productList,
        "Product-count":len(productList)
    }
    

def updateProduct(req: Request, body: ProductSchema, db: Session, user: User):
    product_id = req.query_params.get("id")
    if not product_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Product ID is required")
    product = db.query(Product).filter(Product.id == int(product_id)).first()
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.user_id != user.id and not user.is_admin:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this product"
        )
    data = body.model_dump()
    for k, v in data.items():
        setattr(product, k, v)
    db.commit()
    db.refresh(product)
    return {
        "Status": "Product is updated...",
        "Product-Details": product
    }


def deleteProduct(req: Request, db: Session, user: User):
    product_id = req.query_params.get("id")
    if not product_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Product ID is required")
    product = db.query(Product).filter(Product.id == int(product_id)).first()
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.user_id != user.id and not user.is_admin:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this product"
        )
    db.delete(product)
    db.commit()
    return {
        "Status": "Product is deleted...",
        "Product-Details": product
    }