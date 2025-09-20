from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.db.db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    mobile = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    hash_password = Column(String)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_seller = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    products = relationship("Product", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    carts = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="categories", passive_deletes=True)

    products = relationship("Product", back_populates="category", passive_deletes=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    in_stock = Column(Integer, default=1)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    category = relationship("Category", back_populates="products", passive_deletes=True)

    user = relationship("User", back_populates="products", passive_deletes=True)

    carts = relationship("Cart", back_populates="product", cascade="all, delete-orphan")

    order_items = relationship("Order", back_populates="product", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
    full_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="address", passive_deletes=True)


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="carts", passive_deletes=True)
    product = relationship("Product", back_populates="carts", passive_deletes=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    count = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="Order Placed")
    address_id = Column(Integer, ForeignKey("address.id"))
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="order_items")
    address = relationship("Address")