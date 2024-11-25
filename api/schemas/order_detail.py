from pydantic import BaseModel
from typing import Optional
from menu_item import MenuItem

class OrderDetailBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    subtotal: float

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = None
    subtotal: Optional[float] = None

class OrderDetail(OrderDetailBase):
    id: int
    menu_item: Optional[MenuItem] = None  # Linking MenuItem to this order detail

    class Config:
        orm_mode = True
