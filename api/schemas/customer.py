from typing import Optional, List
from pydantic import BaseModel
from order import Order
from review import Review
from transaction import Transaction

class CustomerBase(BaseModel):
    address: str

class CustomerCreate(CustomerBase):
    card_number: str
    balance: Optional[float] = 0.00  # This is the default balance. we should change it probably, unless we want to implimet a way to add money(no)

class CustomerUpdate(BaseModel):
    address: Optional[str] = None
    card_number: Optional[str] = None
    balance: Optional[float] = None

class Customer(CustomerBase):
    id: int
    card_number: str
    balance: float
    orders: Optional[List[Order]] = None
    reviews: Optional[List[Review]] = None
    transactions: Optional[List[Transaction]] = None

    class Config:
        orm_mode = True
