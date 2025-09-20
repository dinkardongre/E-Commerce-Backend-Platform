from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str | None = None
    email: str
    mobile: str | None = None
    username: str
    password: str
    is_admin: bool = False
    is_seller: bool = False
    is_active: bool = True


class LoginSchema(BaseModel):
    username : str
    password : str

class CategorySchema(BaseModel):
    name : str
    description : str | None = None

class ProductSchema(BaseModel):
    name : str
    price : int
    description : str | None = None
    in_stock : int
    category_id : int

class AddressSchema(BaseModel):
    city : str
    state : str
    pincode : str
    full_address : str

class CartSchema(BaseModel):
    product_id : int
    quantity : int

class OrderSchema(BaseModel):
    address_id : int