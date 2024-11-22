from pydantic import BaseModel
from typing import List

class OrderPromotionBase(BaseModel):
    order_id: int
    promotion_id: int

class OrderPromotionCreate(OrderPromotionBase):
    pass

class OrderPromotion(OrderPromotionBase):
    id: int

    class Config:
        orm_mode = True
