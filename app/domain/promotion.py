from typing import Optional
from pydantic import BaseModel

class PromotionBase(BaseModel):
    burger_id: int
    discount: float
    percentage_discount: Optional[int] = 0
    start_date: str
    end_date: str

class PromotionCreate(PromotionBase):
    pass

class Promotion(PromotionBase):
    id: int

    class Config:
        orm_mode = True

class PromotionResponse(BaseModel):
    burger: str = ""
    discount: str = ""
    percentage_discount: str = ""
    start_date: str = ""
    end_date: str = ""

    def __init__(self,
                 burger: str = "",
                 discount: str = "",
                 percentage_discount: str = "",
                 start_date: str = "",
                 end_date: str = "",
                 **data):
        super().__init__(**data)
        self.burger = burger
        self.discount = discount
        self.percentage_discount = percentage_discount
        self.start_date = start_date
        self.end_date = end_date