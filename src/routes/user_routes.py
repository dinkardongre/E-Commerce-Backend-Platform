from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.utils.dtos import UserSchema, LoginSchema, ProductSchema,AddressSchema,CartSchema,OrderSchema
from src.db.db import get_db
from src.controllers.user_controller import *
from src.controllers.category_controller import *
from src.controllers.product_controller import *
from src.controllers.address_controller import *
from src.controllers.cart_controller import *
from src.controllers.order_controller import *
from src.middlewares.auth_middleware import is_authenticated, is_admin, authorize_admin_or_seller
from src.models.user_model import User

userRouter = APIRouter(prefix="/users")

@userRouter.get("/")
def get_all(db:Session = Depends(get_db), user:User = Depends(is_admin)):
    return getAllUsers(db, user)

@userRouter.post("/register")
def register_user(body:UserSchema, db:Session = Depends(get_db)):
    return register(body, db)

@userRouter.post("/login")
def login_user(body:LoginSchema, db:Session = Depends(get_db)):
    return login(body, db)

@userRouter.get("/profile")
def fetch_profile(user:User = Depends(is_authenticated)):
    return fetchMyProfile(user)

@userRouter.put("/")
def update_user(body:UserSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return updateUser(body, db, user)

@userRouter.delete("/")
def delete_user(db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return deleteUser(db, user)

@userRouter.post("/category")
def create_category(body:CategorySchema,db:Session = Depends(get_db), admin_user : User = Depends(is_admin)):
    return createCategory(body, db,admin_user)

@userRouter.get("/categories")
def get_all_category(db:Session = Depends(get_db)):
    return getAllCategories(db)

@userRouter.put("/category")
def update_category(body:CategorySchema,db:Session = Depends(get_db), admin_user : User = Depends(is_admin)):
    return updateCategory(body, db, admin_user)

@userRouter.put("/update/{user_id}")
def update_user_by_admin(
    user_id: int,
    body: UserSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_authenticated),
):
    return updateUserByAdmin(user_id, body, db, current_user)


@userRouter.delete("/update/{user_id}")
def delete_user_by_admin(user_id:int, db:Session = Depends(get_db), current_user:User = Depends(is_authenticated)):
    return deleteUserByAdmin(user_id, db, current_user)

@userRouter.delete("/category")
def delete_category(db:Session = Depends(get_db), admin_user : User = Depends(is_admin)):
    return deleteCategory(db, admin_user)

@userRouter.post("/product")
def create_product(body:ProductSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return createProduct(body, db, user)

@userRouter.get("/products")
def getAll_products(req:Request = None, db:Session = Depends(get_db)):
    return getProducts(req, db)

@userRouter.put("/product")
def update_product(req:Request, body:ProductSchema, db:Session = Depends(get_db), user:User = Depends(authorize_admin_or_seller)):
    return updateProduct(req, body, db, user)

@userRouter.delete("/product")
def delete_product(req:Request, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return deleteProduct(req, db, user)

@userRouter.post("/address")
def add_address(body:AddressSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return addAddress(body, db, user)

@userRouter.put("/address")
def update_address(body:AddressSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return updateAddress(body, db, user)

@userRouter.delete("/address")
def delete_address(db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return deleteAddress(db, user)

@userRouter.get("/address")
def get_all_address(db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return  getAllUsersAddress(db, user)

@userRouter.post("/cart")
def add_products_to_cart(body:CartSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return addCart(body, db, user)

@userRouter.get("/cart")
def get_all_cart_items(db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return getAllCartItems(db, user)

@userRouter.put("/cart/{cart_id}")
def update_cart_items(cart_id, body:CartSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return updateCartItem(cart_id,body, db, user)

@userRouter.delete("/cart/{cart_id}")
def delete_cart_items(cart_id:int, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return deleteCartItem(cart_id, db, user)

@userRouter.post("/order")
def place_orcer(body:OrderSchema, db:Session = Depends(get_db), user:User = Depends(is_authenticated)):
    return placeOrder(body, db, user)