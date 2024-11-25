from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from order import Order

class PromotionBase(BaseModel):
    code: str
    discount_amount: float
    expiration_date: date
    is_active: Optional[bool] = True

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    discount_amount: Optional[float] = None
    expiration_date: Optional[date] = None
    is_active: Optional[bool] = None

class Promotion(PromotionBase):
    id: int

    class Config:
        orm_mode = True

class PromotionWithOrders(Promotion):
    orders: List["Order"]

    class Config:
        orm_mode = True