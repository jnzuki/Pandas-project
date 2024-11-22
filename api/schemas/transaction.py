from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .customer import Customer

class TransactionBase(BaseModel):
    card_number: str
    transaction_type: str
    transaction_date: Optional[datetime] = None
    amount: float
    balance_after_transaction: float

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    card_number: Optional[str] = None
    transaction_type: Optional[str] = None
    transaction_date: Optional[datetime] = None
    amount: Optional[float] = None
    balance_after_transaction: Optional[float] = None

class Transaction(TransactionBase):
    id: int
    customer: Customer

    class Config:
        orm_mode = True
