from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .order_detail import OrderDetail
from .promotion import Promotion

class OrderBase(BaseModel):
    customer_id: int
    order_date: Optional[datetime] = None
    status: Optional[str] = "pending"
    total_amount: Optional[float] = 0.0
    delivery_type: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None
    delivery_type: Optional[str] = None

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    order_details: List[OrderDetail] = []
    promotions: List[Promotion] = []

    class Config:
        orm_mode = True