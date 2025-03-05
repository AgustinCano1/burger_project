from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db import connection

class Burger(connection.Base):
    __tablename__ = "BURGER"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    active = Column(Integer, default=1)
    ingredients = relationship("BurgersIngredients", back_populates="burger")
    stores = relationship("StoresBurgers", back_populates="burger")

class Ingredient(connection.Base):
    __tablename__ = "INGREDIENTS"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    active = Column(Integer, default=1)
    burgers = relationship("BurgersIngredients", back_populates="ingredient")

class BurgersIngredients(connection.Base):
    __tablename__ = "BURGERS_INGREDIENTS"
    id = Column(String, primary_key=True, index=True)
    burger_id = Column(Integer, ForeignKey("BURGER.id"))
    ingredient_id = Column(Integer, ForeignKey("INGREDIENTS.id"))
    quantity = Column(Integer, default=1)
    burger = relationship("Burger", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="burgers")

class Store(connection.Base):
    __tablename__ = "STORES"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    is_24hrs = Column(Integer, default=0)
    has_drive_thru = Column(Integer, default=0)
    monday = Column(Integer, default=0)
    tuesday = Column(Integer, default=0)
    wednesday = Column(Integer, default=0)
    thursday = Column(Integer, default=0)
    friday = Column(Integer, default=0)
    saturday = Column(Integer, default=0)
    sunday = Column(Integer, default=0)
    burgers = relationship("StoresBurgers", back_populates="store")

class StoresBurgers(connection.Base):
    __tablename__ = "STORES_BURGERS"
    id = Column(String, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("STORES.id"))
    burger_id = Column(Integer, ForeignKey("BURGER.id"))
    active = Column(Integer, default=1)
    store = relationship("Store", back_populates="burgers")
    burger = relationship("Burger", back_populates="stores")

class Promotion(connection.Base):
    __tablename__ = "PROMOTIONS"

    id = Column(Integer, primary_key=True, index=True)
    burger_id = Column(Integer, ForeignKey("BURGER.id"), nullable=False)
    discount = Column(Float, nullable=False)
    percentage_discount = Column(Integer, default=0)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
