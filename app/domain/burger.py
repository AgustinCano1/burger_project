from typing import Optional
from pydantic import BaseModel

class BurgerBase(BaseModel):
    description: str = ""
    price: str = ""

    def __init__(self,
                 description: str = "",
                 price: str = "",
                 **data):
        super().__init__(**data)
        self.description = description
        self.price = price

class BurgerCreate(BurgerBase):
    description: Optional[str] = None
    active: Optional[bool] = True

class Burger(BurgerCreate):
    id: int

    class Config:
        orm_mode = True

class BurgerResponse(BaseModel):
    description: str = ""
    price: str = ""
    ingredients: list = []
    stores: list = []
    promotions: list = []

    def __init__(self,
                 description: str = "",
                 price: str = "",
                 ingredients: list = None,
                 stores: list = None,
                 promotions: list = None,
                 **data):
        super().__init__(**data)
        self.description = description
        self.price = price
        self.ingredients = ingredients
        self.stores = stores
        self.promotions = promotions